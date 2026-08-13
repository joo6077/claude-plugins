---
feature: "카이젠 Phase 2 — 계약 봉인(F2) + 측정 커버리지 검출기(F1) + 인자 매트릭스(F3) + 음성 대조"
created: "2026-08-13 09:55"
complexity: "복잡"
conditions: 26
slug: kaizen-phase2-contract-seal
status: done
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:6879cf9887caebd6
locked_at: "2026-08-13 09:55"
---

## 배경

`.harness/.meta/evidence/phase2.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

**F2 가 최우선이고, F2 의 처리 방식이 이번 스프린트의 성패를 가른다.** 직전 사이클(2026-07-28)이
amendment 사이드카를 도입했는데도 2026-08-11 에 `AR-04: 계약 write-once 위반 — 생성자가 자신이 만든
산출물을 사후에 허용하려 계약 AR-04 조건 문구를 직접 편집(5→7 경로)` 이 관측됐다. 문장을 한 줄 더
추가하면 6 번째 재발이 난다. 따라서 **근본원인 3 개를 먼저 규명하고 등급을 올린다.**

### F2 근본원인 (전부 실측)

| # | 근본원인 | 실측 증거 |
| --- | --- | --- |
| RC1 | **write-once 규칙이 쓰기 측 표면에 존재하지 않는다** | `grep -rn 'write-once'` 결과 — qa-evaluator.md:566 · qa-evaluation-guide.md:350 (**읽기 측 2 건**) / contract-design-guide.md · sprint-contract/SKILL.md (**쓰기 측 0 건**). 본문을 편집한 주체는 "생성자" 인데 생성자가 읽는 문서 어디에도 그 규칙이 없다 |
| RC2 | **준수 경로(사이드카)의 기대 보상이 위반 경로보다 낮다** | 같은 날 REJECT — `amendment A-01은 prompt-log 앵커 부재로 unknown 분류, PASS 근거 불가`. 사이드카를 실제로 썼는데 앵커가 없어 `unknown` 으로 떨어져 아무 효력이 없었다. 다음 시도에서 본문 직접 편집으로 전환됐다 |
| RC3 | **위반이 탐지되지 않는다** | 계약 본문은 평문 markdown 이고 변조를 재는 오라클이 없다. Step 6.5 게이트는 헤더·조건 수만 본다 — 조건 **문구** 가 바뀌어도 조건 수가 같으면 통과한다 |

RC2 의 구조를 한 줄로: `유형` 이 direction(강화/완화)과 consent(앵커 유무)를 **한 축에 뭉쳐** 놓아서,
앵커가 없다는 이유만으로 방향 판정까지 `unknown` 으로 붕괴했다. 두 축은 독립이다.

### 처리 방침 — 문장 추가가 아니라 등급 상향

- RC3 → **E1 서술 → E3 결정론적 게이트**: 계약 봉인(`conditions_digest`). 조건 체크박스 줄만
  정규화 해시하므로 체크박스 토글·서술 편집은 통과하고 조건 문구 변조·조건 추가는 즉시 깨진다.
- RC1 → 쓰기 측 3 표면(가이드·스키마·SKILL.md)에 동일 규약을 착지. 읽기 측 용어를 바꾸지 않는다.
- RC2 → amendment 를 **direction × consent 2 축**으로 분리. 경로 화이트리스트의 direction 은
  집합 비교로 **계산**한다 (5→7 은 계산상 `relaxing` — 자기신고 여지 없음).

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase2.md` §1~§6 (URL·수치·조항 초안·금지 목록·트레이드오프 전부 여기서만)
- `.harness/.meta/kaizen-data-pool.md` §1 — REJECT `AR-04`(4 건) / `LG-01` / `ER-02` / `UI-04`,
  Improvement `[AR-04] 계약-측정-불일치` / `[LG-02, LG-04] write-once 원문` / `audience_matrix 6 relation`
- `.claude/kaizen-input/insights-report.md` — 직전 사이클 흡수분 표 + 신규 델타 D2
- `docs/kaizen/changelog.md` `[2026-07-28]` — 사이드카 도입분 (재승격 금지 대상)
- Phase 1 산출물 `harness/docs/guides/skill-design-guide.md` §3.7 등급 원장 · §5.6 Variant Budget

## GAP 분석 (전부 실측)

| # | 갭 | 실측 근거 | 처리 |
| --- | --- | --- | --- |
| G1 | 계약 변조 탐지 오라클 부재 | Step 6.5 3 명령 중 조건 문구를 재는 것 0 개 | 봉인(E3) 신설 |
| G2 | write-once 가 쓰기 측 0 건 | `grep -rn 'write-once'` 쓰기 측 2 파일 0 건 | 3 표면 착지 |
| G3 | amendment 유형이 1 축 3 값이라 앵커 부재가 방향 판정을 붕괴시킴 | REJECT `amendment A-01 ... unknown 분류` | direction × consent 2 축 |
| G4 | 산문 대상 ↔ 측정 대상 커버리지 갭을 재는 수단 없음 | Improvement `[AR-04] 계약-측정-불일치 — 프로즈 12 항목 vs 측정 5 개 디렉토리` | 검출기(E2) 신설 |
| G5 | 조합 케이스 수를 사람이 타이핑 | REJECT `3 visibility x 6 relation = 18 중 15 만 재현` · `16 종 중 2 종만 검증` | 인자 매트릭스 신설 |
| G6 | variant 축 값 상이성이 계약 레벨에서 안 잡힘 | REJECT `UI-04: B3 과 B6 이 4 축 전부 동일값` | 인자 매트릭스의 두 번째 용법 |
| G7 | 측정문이 구현 제거에 반응하는지 안 본다 | REJECT `ER-02: mutation test 로 확정 — 동시성 가드를 완전히 삭제해도 테스트 통과` | 음성 대조 신설 |
| G8 | QA 모호성 태그가 작성 단계로 되먹여지지 않음 | Improvement 태그 6 종 반복 (`측정-수단-부재` 외) | 작성 preflight 로 승격 |
| G9 | 가이드 버전 정보가 실제 스키마와 drift | `contract-design-guide.md:916` = `v4`, 실제 스키마 = v5.2 | 사실 정정 |
| G10 | parity 대상 버전이 Phase 1 bump 이전 값 | `:917` = skill v1.4.0 / agent v1.5.0, Phase 1 이 1.5.0 / 1.6.0 으로 bump | 사실 정정 |

### 오라클 유효성 사전 검증 (직전 사이클 최대 교훈 — 실행 결과만이 증거)

계약 작성 **전에** 오라클 후보를 실제 계약 109 개에 걸어 오탐률을 측정했다.

- **봉인 오라클**: 기존 계약 109 개 × zsh·bash → `absent=109 ok=0 broken=0`. 오탐 0.
  변조 시나리오 5 종에서 (체크박스 토글 OK · 서술 편집 OK · 조건 문구 변조 BROKEN ·
  조건 추가 BROKEN) 로 의도대로 갈렸다.
- **커버리지 오라클**: enumerated 조건 114 개 대상. 나이브(백틱 토큰 전부·1 개 이상) 는
  **76/114 = 67% flagged** 로 사실상 전건 경보다. 경로형 토큰 + 2 개 이상으로 좁히면
  **29/114 = 25%**. 표본 확인 결과 상당수가 "상위 명령이 덮는" 정당 케이스였다.
  → **blocking 게이트로 쓰면 안 된다.** evidence §5 의 "검출기 + 사람의 해소 기록" 지침대로
  E2 검출기로 착지하고, `UNCOVERED` 1 건마다 수정 또는 해소 기록을 요구한다.
- **direction 계산기**: AR-04 실사례(3 → 5 경로)를 `relaxing added=2 removed=0` 으로 계산.
  자기신고 여지가 없다.
- **variant 중복 검출기**: UI-04 실사례(B3·B6 4 축 동일)를 `DUP_AXIS ... ← variants: B3 B6` 로 재현.

## 범위 경계

- 수정 허용 3 경로: `harness/docs/guides/contract-design-guide.md` ·
  `harness/skills/sprint-contract/SKILL.md` · `harness/references/contract-schema.md`.
  계약 파일 `.harness/sprint-contract-kaizen-phase2-contract-seal.md` 만 예외.
- **소비면(`harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md`)은
  이번 스프린트 scope 밖**이다 (Phase 3 소관). 미완 조건으로 명시한다 — `[미검증]` 이 아니다.
- 기존 계약 109 개와 `harness/scripts/*.sh` 는 **무수정**이며 동작이 바뀌지 않아야 한다.

### 커버리지 해소 기록 (검출기 출력 대응 · 봉인 후 추가)

검출기가 이 계약에서 `UNCOVERED` 1 건을 냈다. 조건 줄은 봉인되어 고칠 수 없으므로(그리고 고칠
필요도 없으므로) 여기에 해소 기록을 남긴다 — **서술 섹션 편집은 봉인을 깨지 않는다.**

- **커버리지 해소: AR-02 — 정당 (조건의 주어와 대상이 같은 토큰)**. 산문 측 4 토큰
  (`skill-design-guide.md` · `agent-design-guide.md` · `harness/references/contract-schema.md` ·
  `harness/docs/guides/contract-design-guide.md`) 은 **값을 추출할 원본 파일**이고, 측정 절은
  그 4 개를 "세 파일에서 값을 각각 추출해 문자열 비교" 로 집합 지칭한다. 실제 검증에서 네 값을
  전부 추출해 비교했다 (schema `v5.3` MATCH · parity `1.5.0`/`1.6.0` MATCH). 이 형태가 실측
  오탐 25% 의 전형이며, 그래서 검출기를 blocking 으로 올리지 않았다.

### 열린 질문에 대한 결정 (evidence §6 — 근거를 남긴다)

1. **경로 화이트리스트 판정 기준** — 단일 기준으로 고정하지 **않는다.** 실측 REJECT 4 건 중 2 건은
   커밋 후(`git show --name-only`), 2 건은 미커밋 상태에서 측정됐다. 하나를 강제하면 반대편이 항상
   어긋난다. 기존 Diff-Scope 표준형의 `Given:` 이 이미 상태를 고정하므로, **`scope_allowlist`
   조건은 그 `Given` 에 맞는 명령을 정확히 1 개만 갖는다** 로 규정한다.
2. **`relaxing` 승인 주체** — 사용자 명시 승인(앵커)만. reviewer 확인은 요구하지 않는다.
   parity item 12 의 착지 구조상 평가자는 계약에 없는 요구를 만들지 않는 것이 원칙이다.
3. **조합 기본값** — full Cartesian 이 기본. pairwise 로 낮추려면 곱셈 결과와 사유를 서술 절에
   기록하고 사용자 승인을 받는다. 임계 숫자를 지어내지 않는다.

## 회귀 게이트

- 신규 frontmatter 2 필드(`conditions_digest` · `locked_at`)는 **선택 필드**다. 부재 시
  `SEAL_ABSENT` 경고이지 실패가 아니며 ladder 판정을 바꾸지 않는다.
- 신규 셸 스니펫은 전부 zsh·bash 동일 출력이어야 한다 (글로빙 금지 · 배열 전달 규약 준수).

## Architecture

- [ ] AR-01: 스프린트 변경이 정확히 4 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: `git status --porcelain` 출력이 정확히 4 행이고 경로 집합이
       `harness/docs/guides/contract-design-guide.md`,
       `harness/skills/sprint-contract/SKILL.md`,
       `harness/references/contract-schema.md`,
       `.harness/sprint-contract-kaizen-phase2-contract-seal.md` 와 정확히 일치)
- [ ] AR-02: `harness/docs/guides/contract-design-guide.md` 의 버전 정보 3 행이 실제 값과 일치한다
      — Schema version 이 `harness/references/contract-schema.md` 의 `## 스키마 버전 > 현재:` 값과
      동일하고, Parity with 가 `skill-design-guide.md` / `agent-design-guide.md` frontmatter 의
      `version` 값과 동일하다 [exact, enumerated]
      (측정: 세 파일에서 값을 각각 추출해 문자열 비교 — 불일치 0 건. 손으로 타이핑한 값 비교 금지)
- [ ] AR-03: 기존 계약 109 개에 봉인 검사를 걸었을 때 `SEAL_BROKEN` 이 0 건이고 전부
      `SEAL_ABSENT` 로 분류된다 (하위호환) [exact]
      (Given: 이번 스프린트 계약 파일 제외 ·
       측정: `.harness` 하위 계약을 `find` 로 열거해 봉인 검사 실행 — zsh·bash 양쪽에서
       `broken=0` 이고 `absent` 수가 열거 파일 수와 같다)
- [ ] AR-04: 신규 frontmatter 2 필드를 삽입해도 기존 reader 의 판정이 바뀌지 않는다 [exact]
      (측정: 계약 사본에 `conditions_digest` · `locked_at` 을 넣고 `fm_get` 으로
      `slug` / `status` / `owner_session` 3 값을 읽어 삽입 전과 **문자열 동일**,
      contract-schema §ladder 판정 스니펫 출력도 삽입 전후 동일)
- [ ] AR-05: 소비면 2 파일이 이번 scope 밖임을 명시적 미완 조건으로 남긴다 [structural, enumerated]
      (측정: 계약 서술 절 §범위 경계 에 `harness/agents/qa-evaluator.md` ·
      `harness/docs/guides/qa-evaluation-guide.md` 2 경로가 각각 이름으로 등장하고
      Phase 3 소관임이 명시된다. `[미검증]` 마커를 쓰지 않는다)
- [ ] AR-06: 계약 레이어 등급표가 `skill-design-guide.md` §3.7 등급 원장을 복제하지 않고
      참조 관계를 명시한다 [structural]
      (측정: contract-design-guide 등급표 절에 "원장" 과 "§3.7" 이 같은 절에 등장하고,
      §3.7 원장 8 행의 원칙명이 계약 등급표에 등급값과 함께 재기재된 행 0 건)

## Skill

- [ ] SK-01: `harness/skills/sprint-contract/SKILL.md` 에 계약 봉인 Step 이 신설되고 4 요소를
      모두 담는다 — (a) 정규화 digest 계산 함수 (b) frontmatter 2 필드 기록
      (c) 기록 직후 자기 검증 (d) 봉인 이후 조건 본문 편집 금지 명시
      [structural, enumerated] (측정: 해당 Step 구간 안에서 4 요소 각각 1 건 이상 grep)
- [ ] SK-02: Step 0.5 (c) 의 `TAKEN` 분기에서 기존 계약의 봉인을 검증하고 `SEAL_BROKEN` 시
      사용자에게 보고하도록 절차가 추가된다 [exact]
      (측정: Step 0.5 (c) 구간에 `SEAL_BROKEN` 문자열 1 건 이상)
- [ ] SK-03: Gotchas 에 이번 사이클 신규 하드 규칙 3 항이 각각 1 줄 이상으로 존재한다
      — write-once 봉인 · 음성 대조 · 인자 매트릭스 [structural, enumerated]
      (측정: `## Gotchas` 헤더와 그 다음 2 단계 헤더 사이 구간에서 `봉인` · `음성 대조` ·
      `인자 매트릭스` 각각 1 건 이상)
- [ ] SK-04: 저장 검사 게이트에 커버리지 검출기가 추가되고 **blocking 아님**이 명시된다 [exact]
      (측정: 게이트 Step 구간에 `UNCOVERED` 1 건 이상 AND 같은 구간에 "해소 기록" 이 등장)
- [ ] SK-05: Step 7 자기진단 체크리스트에 이번 신규 항목 5 개가 추가된다
      — `contract_seal_missing` · `measurement_coverage_gap` · `factor_matrix_missing` ·
      `negative_control_missing` · `amendment_direction_uncomputed` [exact, enumerated]
      (측정: Step 7 구간에서 5 개 식별자 각각 1 건 이상)

## Script

- [ ] SC-01: 봉인 스니펫이 변조 시나리오 5 종에서 zsh·bash 동일한 결과를 낸다 [exact, enumerated]
      (측정: 봉인 직후=`SEAL_OK` · 체크박스 토글 후=`SEAL_OK` · 조건 문구 변조 후=`SEAL_BROKEN` ·
      조건 추가 후=`SEAL_BROKEN` · 서술 절 편집 후=`SEAL_OK` — 5 행이 두 셸에서 동일)
- [ ] SC-02: 커버리지 검출기가 zsh·bash 동일 출력이고, 실측 flag rate 가 가이드에 기록된다 [exact]
      (측정: 계약 109 개 대상 두 셸 실행 결과 요약 행이 동일 AND contract-design-guide 에
      나이브 대비 좁힌 변형의 flagged 수치 2 개가 등장)
- [ ] SC-03: variant 축 중복 검출기가 REJECT `UI-04` 실사례를 재현한다 [exact]
      (측정: 4 축 튜플 4 행 입력에서 중복 1 건 검출 + 해당 variant ID 2 개 출력, zsh·bash 동일)
- [ ] SC-04: amendment direction 계산기가 REJECT `AR-04` 실사례(3 → 5 경로)를 `relaxing` 으로
      판정한다 [exact]
      (측정: 원 집합 3 행 · 개정 집합 5 행 입력에서 `relaxing added=2 removed=0`, zsh·bash 동일)

## Error

- [ ] ER-01: evidence §4 금지 5 항이 이번 신규 서술에 0 건이다 [exact, enumerated]
      — (a) "측정이 조건 의도를 커버하는지 확인하라" 류 한 줄 Gotcha 만 추가 (b) LLM 에게
      "모호한가?" 만 묻는 게이트 (c) 사람이 숫자를 옮겨 적는 필드 신설 (d) `relaxing` 을 조용히
      최신 계약으로 간주 (e) path whitelist 를 자연어와 grep 양쪽에 중복 관리
      (측정: 각 항목에 대응하는 반증 서술이 신규 절에 존재함을 `파일:라인` 으로 제시)
- [ ] ER-02: 커버리지 검출기가 blocking 판정기가 아니라 "검출기 + 해소 기록" 으로 규정되고,
      그 근거로 실측 오탐률이 함께 기록된다 [exact]
      (측정: contract-design-guide 해당 절에 "blocking" 부정 서술 1 건 + flagged 수치 1 건)
- [ ] ER-03: `harness/references/contract-schema.md` 의 스키마 버전이 bump 되고 변경 이력에
      이번 사이클 항목이 1 행 추가된다 [exact]
      (측정: `## 스키마 버전 > 현재:` 값이 v5.2 가 아니고, `변경 이력` 최상단 항목이 신규 버전)

## Anti-patterns

- [ ] AP-03: 세 문서의 신규 코드 펜스에 언어 힌트가 있다 — bare fence 0 건
      (측정: 펜스 길이 인식 검출기로 여는 펜스 중 힌트 없는 것 0 건)
- [ ] AP-04: `harness/skills/sprint-contract/SKILL.md` frontmatter 의 `name` 필드가 보존된다
      (측정: 첫 frontmatter 블록에서 `name: sprint-contract` 1 건)

## Reusability

- [ ] RE-01: 신규 셸 스니펫이 기존 규약을 재사용한다 — `fm_get` 동일 구현 · `find` 열거 ·
      조건 grep 패턴 `[A-Z]{2,}-[0-9]{2}` 재사용 [structural, enumerated]
      (측정: 신규 스니펫에서 3 요소 각각 1 건 이상, 새 패턴 발명 0 건)
- [ ] RE-02: 해시 계산이 기존 fallback 사슬 관행을 따르고 4 백엔드가 동일 값을 낸다
      (측정: `sha256sum` / `shasum` / `python3` / `openssl` 4 경로가 같은 입력에 동일 출력)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py harness` 가 FAIL 0 건
      (측정: 명령 실행 후 종료 코드 0 · FAIL 행 0)
- [ ] DG-02: 세 문서의 신규 `bash` 코드 펜스가 `bash -n` 구문 검사를 통과한다 (IDE 진단 대체 —
      이 레포는 셸/문서 기반이라 IDE 진단 대상 소스가 없다)
      (측정: 펜스 본문을 추출해 `bash -n` 실행 — 에러 0 건)
- [ ] DG-03: `python3 scripts/sync-docs.py --check-only` 가 이번 변경으로 인한 README 갱신 필요를
      보고하지 않는다
      (측정: 명령 출력에 scope 3 파일 소속 플러그인의 갱신 필요 항목 0 건)
- [ ] DG-04: 신규 셸 스니펫 전수가 zsh·bash 양쪽에서 실행 성공한다 (앱 구동 대체 — 이 레포에는
      구동 대상 앱/서버가 없다)
      (측정: 스니펫별 두 셸 실행 결과 비교 — 실패 0 건 · 출력 불일치 0 건)
