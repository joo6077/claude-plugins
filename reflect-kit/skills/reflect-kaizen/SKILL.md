---
name: reflect-kaizen
description: >
  reflect-kit 파이프라인 자체의 품질을 월 1회 측정·보정한다.
  (1) 최근 reflections 랜덤 10건을 독립 LLM(Haiku 또는 다른 모델)에 재분류 요청하여 원 분류와의 일치도 측정,
  (2) 70% 미만 시 log-reflection.sh 의 분석 프롬프트 개선 트리거,
  (3) promotions-ledger.md 의 post_freq 를 30일 뒤 재측정하여 회귀 규칙 demotion 후보 표시,
  (4) precedence table 의 freq 임계값(2회/3회) hypothesis 를 pre/post 재발률로 calibrate 한다.
  "reflect 카이젠", "reflection 품질 점검", "regression 측정", "calibration",
  "ledger post_freq 업데이트", "reflection 프롬프트 개선" 요청 시 트리거.
  harness-kaizen / contract-kaizen / evaluator-kaizen 과 도메인이 다르므로 혼동하지 않는다.
argument-hint: "[project=<id>] [window=<30d|60d|90d>] [sample=<int>]"
user-invocable: true
---

# Reflect Kaizen

reflect-kit 자체를 자기 점검하는 스킬. digest/promote 가 실수 규칙을 쌓는 동안, 이 스킬은 그 규칙들이 실제로 재발을 줄였는지, 분류 품질이 떨어지지 않았는지, 임계값이 여전히 타당한지를 주기적으로 측정한다.

**도메인 구분**: harness-kaizen 은 QA/Contract/Evaluator 를, contract-kaizen 은 Sprint Contract 를, evaluator-kaizen 은 QA Evaluator 를 개선한다. 이 스킬은 **reflect 파이프라인의 분류·승격 품질**을 개선한다. 개선 대상이 다르므로 출력도 서로 참조하지 않는다.

## Gotchas

1. **LLM-as-judge 는 다른 모델로 실행**. 원 분류가 codex(GPT-5급)로 이루어졌다면 재분류는 Haiku 또는 다른 engine 으로. 같은 모델로 재분류하면 self-consistency 측정이 되어 judge 가치가 떨어진다.
2. **10건 중 7건 일치(70%) 는 경계치 hypothesis**. 실제 일치도가 60~80% 사이라면 샘플을 늘려 다시 측정한 뒤 프롬프트 수정 여부를 결정하라. 작은 표본으로 프롬프트를 매번 흔들면 드리프트 위험.
3. **post_freq 측정은 `promoted_at + 30d` 이후에만 의미 있다**. 그전에 측정하면 calibration window 미충족으로 숫자가 편향된다. 20일 시점의 post_freq 를 근거로 demotion 을 제안하지 마라.
4. **임계값 변경은 프롬프트/스킬 변경보다 보수적**. freq 2 → 3 로 올리면 과거에 이미 승격된 규칙들의 정당성이 흔들리고, 1 → 2 로 내리면 false positive 가 급증한다. 최소 60일 이상의 pre/post 재발률 비교 데이터가 있어야 변경 제안.
5. **프롬프트 개선 제안은 diff 로 제시하고 자동 저장 금지**. `log-reflection.sh` 의 프롬프트 블록을 직접 수정하려면 사용자가 diff 를 읽고 승인해야 한다. kaizen 이 훅 스크립트를 자동 변경하면 드리프트 감지가 어렵다.
6. **"no issues" 만 나오는 기간은 정상 또는 프롬프트 실패 둘 다 가능**. 연속 4주 모두 no issues 면 프롬프트가 과도하게 엄격해졌을 가능성을 의심하라 (false negative).
7. **`post_freq` 는 `canonical_tag` 단독이 아니라 `lemma_key` 클러스터 전체(canonical + aliases)로 센다**. ledger 엔트리의 `aliases` 를 무시하면 같은 근본원인이 다른 표기로 재발했을 때 0 으로 집계되어 **효과 없는 규칙이 "효과 있음" 으로 오판정**된다. 집계는 반드시 `${CLAUDE_PLUGIN_ROOT}/hooks/_lib-tag-canon.sh` 의 `tag_canon_groups` 출력으로 한다 — 눈으로 세지 마라. 2026-08-13 실측: `skipped-required-api-doc-check` 원시 단독 71 vs 클러스터 110 (39 건 = 55% 누락).
8. **LLM-as-judge 재분류 프롬프트에는 기존 태그 어휘를 주입하지 마라**. `log-reflection.sh` 는 canonicalization 을 위해 어휘를 주입하지만, judge 에 같은 어휘를 주면 judge 가 원 분류의 태그를 그대로 베껴 일치도가 인위적으로 올라간다. judge 는 **어휘 없이** 재분류해야 측정이 오염되지 않는다. 단 `mistake_tag` 일치는 원래 semantic 비교이므로 표기가 달라도 같은 의미면 일치로 센다.
9. **파편화 판정에 `fold_ratio`(원시/클러스터)를 쓰지 마라 — `singleton_share` 를 써라**. 클러스터링이 아무것도 못 묶으면 `fold_ratio` 는 **1.00 이 되어 항상 "정상"** 이다. 2026-08-13 전량 실측이 그 상태였다: `fold_ratio 1.02` 인데 클러스터 2,578 개 중 2,279 개가 1 회짜리(`singleton_share 0.884`). `tag_canon_fragmentation` 을 매 사이클 실행하고 `singleton_share > 0.70`(**hypothesis** — baseline 0.884, 이 스킬이 calibrate)이면 어휘 수렴이 실패한 상태다. 이 지표가 나쁘면 다른 모든 측정(post_freq, 임계값 calibration)의 신뢰도가 함께 떨어지므로 **먼저** 확인한다.
10. **`actionability: user_environment` 엔트리를 품질 측정 모수에 넣지 마라**. Stop 훅 dedup 게이트가 억제하므로 reflections 본문의 표본이 실제 발생과 다르다. judge 샘플링·재발률 집계는 `claude_behavior` 만 대상으로 한다. 환경 이슈 규모는 `.env-issues.tsv` 의 `count` 로 별도 보고.
11. **`user_stated_constraint == true` fast-track(precedence #0)은 별도 효과 측정 대상**. freq 임계값을 우회해 첫 재위반부터 CLAUDE.md/hook로 승격하므로, calibration 시 이 surface로 간 규칙의 post_freq 를 일반 freq 승격과 분리 집계하라. fast-track 후 post_freq 가 0 으로 잘 떨어지면 Friction #2(피드백 durable 미반영)가 완화된 증거다. 떨어지지 않으면 surface 가 약했거나(memory 로 잘못 감) 규칙 문구가 모호한 것 — 표시.
12. **파편화 임계 초과 상태에서 demotion 후보를 내지 마라.** 그 상태의 `post_freq` 는 구조적 과소집계이고, `post_freq == 0` 은 "효과 있음" 이 아니라 "못 셌음" 이다. §0 이 `calibration_confidence: low` 를 선언하면 **(2) Ledger Calibration 표의 `verdict` 에 `demote-candidate` 를 쓸 수 없다** — `blocked-low-confidence` 로 적는다. 이것은 서술 권고가 아니라 산출 금지다.

## 입력

- `project` (optional): 대상 프로젝트 ID. 없으면 현재 cwd 기준.
- `window` (optional): `30d` / `60d` / `90d`. 기본 `30d` (post_freq 측정 창).
- `sample` (optional): LLM-as-judge 샘플 크기. 기본 10.

## Process

### 0. 파편화 지표 선행 확인 — **여기서 calibration 유효성이 결정된다**

이 단계는 리포팅이 아니라 **게이트**다. 여기서 `low` 가 나오면 3 단계의 demotion 산출이 금지된다.

```bash
# 절대경로로 source 한다. cd 로 cwd 를 맞추지 마라 — SSOT §6.1 (cwd 의존은 무증상 실패다).
. "${CLAUDE_PLUGIN_ROOT}/hooks/_lib-tag-canon.sh"
tag_canon_selftest      # 양성 대조 — SELFTEST_OK 가 아니면 아래 지표는 무의미하다
tag_canon_fragmentation ~/.claude/logs/<bucket>/reflections-*.md
# raw_distinct \t clusters \t entries \t singletons \t fold_ratio \t singleton_share \t entries_per_cluster
```

- **`tag_canon_selftest` 가 `SELFTEST_OK` 가 아니면 `calibration_confidence: low` 를 선언한다**
  (SSOT §6.1 규칙 6). 정규화가 죽으면 `singleton_share` 가 **거짓 정상**으로 낮게 나올 수 있고,
  그 경우 이 게이트는 통과하는데 `post_freq` 는 과소집계 상태다 — 게이트가 있는 채로 우회된다.
  selftest 실패는 파편화 임계 초과와 **같은 효력**을 갖는다 (demotion 산출 금지 · 임계 재평가 skip).

- 판정은 **6 열 `singleton_share`** 로 한다. **5 열 `fold_ratio` 로 판정하지 마라** — 클러스터링이 아무것도 못 묶으면 1.00 이라 항상 "정상" 이다 (Gotcha #9).
- `singleton_share > 0.70` (**hypothesis** — 2026-08-13 baseline 0.884) 이면 `calibration_confidence: low` 를 선언한다. 이 선언의 효과는 셋이다:
  1. (2) Ledger Calibration 표 헤더에 `calibration_confidence: low` 를 적는다.
  2. **`demote-candidate` verdict 를 낼 수 없다.** 해당 행은 `blocked-low-confidence` 로 적는다 (Gotcha #12). `post_freq == 0` 은 "효과 있음" 이 아니라 "못 셌음" 이다.
  3. (3) 임계값 재평가를 **건너뛴다** — 과소집계된 재발률로 임계를 흔들면 다음 사이클 판단까지 오염된다.
- 개선 제안(4 단계)의 최우선 항목은 `tag-lemma-map.tsv` 의 `verb-synonym` / `alias` 행 보강이다. 후보는 `/reflect-digest` 의 `## 병합 보류` 와 `new_tag_reason` 목록에서 가져온다.
- 어휘 주입 자체가 작동하는지 확인: `.errors.log` 에 `warn:lemma-map-unreadable` 이 있으면 그 기간은 정규화가 fail-open 이었다. `warn:env-dedup-failed` 가 반복되면 환경 dedup 게이트가 무력화된 것이다.

### 1. LLM-as-judge 재분류

- `~/.claude/logs/<project_id>/reflections-*.md` 에서 최근 `window` 범위 내 YAML 블록을 나열한다. **`actionability: user_environment` 블록은 모수에서 제외**한다 (Gotcha #10).
- 랜덤 `sample` 건 추출. 각 블록의 `trigger / undesired_behavior / desired_behavior / approach_note` 만 남기고 `primary_category / also_applies / mistake_tag / actionability / 4축` 을 제거한 "재분류용 입력" 을 만든다.
- 재분류 프롬프트에 **기존 태그 어휘를 넣지 마라** (Gotcha #8).
- 독립 LLM(Haiku 권장 — 비용 저렴 + 다른 family)에 `log-reflection.sh` 와 동일한 카테고리 정의 + YAML 스키마 프롬프트로 재분류 요청.
- 재분류 결과 YAML 블록 10개를 확보.

### 2. 일치도 측정 + 프롬프트 개선 트리거

- 원 분류와 재분류를 나란히 놓고 다음 항목별 일치도 계산:
  - `primary_category` 일치 (엄격)
  - `mistake_tag` 의 semantic 일치 (같은 의미 다른 표기도 일치로 집계 — 수동 또는 LLM 판단)
  - `actionability` 일치 (엄격) — 불일치가 잦으면 판정 기준 예시가 부족한 것이다
  - 4축 각각의 값 일치
- 전체 일치도(primary_category 기준) `< 70%` 면 **프롬프트 개선 후보**로 표시.
- 어떤 카테고리에서 주로 엇갈리는지 대각 행렬로 요약 (예: misunderstanding 을 wrong_approach 로 분류하는 경향).

### 3. 30일 calibration (ledger post_freq 업데이트)

- `~/.claude/logs/<project_id>/promotions-ledger.md` 읽고 `status: active` + `promoted_at` 이 현재 시점에서 `calibration_window_days` 이상 지난 엔트리 필터링.
- 각 엔트리에 대해:
  - `promoted_at` 이후 기간의 `reflections-*.md` 에서 **`mistake_tag` + `aliases` 전체**의 빈도를 합산 → `post_freq` 에 기록 (Gotcha #7).
  - 합산 중 ledger 의 `aliases` 에 없는 새 표기가 같은 근본원인으로 보이면, 그 태그를 `aliases` 에 **추가**하고 리포트에 "alias 추가" 로 기록한다. 근거 없이 추가하지 마라 — `undesired_behavior` 대조 근거 1줄 필수.
  - `post_freq == 0 AND risk_class == low` → `status: demoted` 후보 표시 (실제 demote 는 `/reflect-promote action=rollback` 에서). **단 §0 이 `calibration_confidence: low` 를 선언했으면 이 후보를 내지 않는다** — `blocked-low-confidence` 로 적는다.
  - `post_freq >= initial_freq` 이고 `promoted_to` 가 `hook` 또는 `*_claude_md` → **`hook-coverage-audit`** verdict. 등급 상향이 아니라 `/reflect-promote` §B-0 의 9 항 점검으로 라우팅한다. 이미 게이트를 걸어 뒀는데 재발이 늘었다면 1 순위 가설은 문구가 아니라 **게이트 미작동**이다.
  - `post_freq == 1` → 문구 명확화 후보(`prompt-revision`). 등급은 올리지 않는다.
  - `post_freq >= 2` → **`enforcement-escalation`** 후보. `harness/docs/guides/skill-design-guide.md` §3.7 승급 규칙에 따라 2회 이상은 E2, 3회 이상이거나 비가역·신뢰 손상이면 E3. 실제 상향은 `/reflect-promote` §B 가 수행한다. 같은 등급에서 문구만 다듬는 제안을 내지 마라.
  - `post_freq < initial_freq AND post_freq <= 1` → 효과 있음, 유지.

### 4. 임계값/프롬프트 개선 제안

- **임계값 재평가**:
  - 60일 이상 누적 데이터에서 `freq == 2` 로 `project_memory` 승격된 규칙들의 30일 재발률 집계.
  - 재발률 > 50% 이고 그 중 상당수가 이후 `project_claude_md` 로 재승격되었다면 → "freq 2 → 2, 3 → 2 로 하향" 제안 (더 빠른 승격).
  - 반대로 대부분 `post_freq == 0` 이고 demoted 후보면 → "freq 2 → 3 로 상향" 제안.
  - 변경 제안은 **DESIGN.md 의 Precedence Table 과 reflect-digest SKILL.md** 두 곳 모두에 반영 필요하다는 사실을 리포트에 명시.
- **프롬프트 개선 제안**:
  - Step 2 결과 대각 행렬에서 혼동 많은 카테고리 쌍을 식별.
  - `log-reflection.sh` 프롬프트의 카테고리 정의에 해당 쌍 구별 기준을 추가하는 diff 초안 작성.
  - 자동 저장하지 말고 사용자에게 제시 → 승인 시 사용자가 직접 반영.

## 출력 포맷

리포트는 아래 6개 섹션을 순서대로 포함한다. 섹션 제목과 표 구조는 고정, 수치는 실제 측정값으로 채운다.

### (0) 파편화 지표

- `tag_canon_fragmentation` 7 열 원문 (raw_distinct / clusters / entries / singletons / fold_ratio / **singleton_share** / entries_per_cluster)
- 판정: `calibration_confidence: high` 또는 `low` (기준 `singleton_share > 0.70`, hypothesis · baseline 0.884)
- `low` 인 경우 **(2) 의 demote-candidate 산출 금지 · (3) 임계값 재평가 skip** 을 리포트에 명시
- `warn:lemma-map-unreadable` 건수 (0 이 아니면 그 기간 정규화가 fail-open)
- 환경 오설정 억제 현황: `.env-issues.tsv` 상위 3건 (tag / count / last_seen)

### (1) LLM-as-judge 일치도

- sample: 10 건 / 모델: haiku-4.5 / 모수: `claude_behavior` 만
- primary_category 일치: 8/10 (80%)
- mistake_tag 일치 (semantic): 6/10 (60%)
- actionability 일치: 10/10 (100%)
- 4축 일치: scope 9/10, risk 7/10, proc 8/10, enforce 10/10
- 혼동 행렬 (primary): 카테고리 쌍별 오분류 수를 `mis | rep | wrong | tool` 4×4 테이블로 표기

### (2) Ledger Calibration (window)

헤더에 `calibration_confidence: high | low` 를 먼저 적는다 (§0 산출).

`| rule_id | canonical_tag | lemma_key | aliases | surface | enforcement_level | initial_freq | post_freq | verdict |` 테이블.
`verdict` 는 `demote-candidate / keep / enforcement-escalation / hook-coverage-audit / prompt-revision / blocked-low-confidence` 중 하나.
`enforcement-escalation` 인 행은 목표 등급(`E2` / `E3`)과 그 근거(재발 횟수 · 비가역성 여부)를 함께 적는다.
`hook-coverage-audit` 인 행은 `/reflect-promote` §B-0 9 항 중 무엇을 확인해야 하는지를 함께 적는다.
`calibration_confidence: low` 이면 `demote-candidate` 는 **한 행도 나올 수 없다**.

### (3) 임계값 재평가 (60d 누적)

- **§0 이 `low` 면 이 섹션을 `skipped (calibration_confidence: low)` 로 적고 수치를 내지 않는다.**
- `freq==2` 로 `project_memory` 승격된 규칙들의 30일 재발률 집계
- 하향(freq 2→1) / 상향(2→3) / 유지 중 하나를 근거와 함께 제안
- `singleton_share` 임계 자체도 calibration 대상이다. baseline 0.884 대비 어디까지 내려갔는지를 기록하고, 2 사이클 이상 데이터가 쌓이기 전에는 임계를 바꾸지 마라

### (4) 프롬프트 개선 제안

혼동 쌍이 있으면 `log-reflection.sh` 프롬프트의 카테고리 정의 블록에 대한 diff 초안을 아래 형식으로 제시:

```diff
--- hooks/log-reflection.sh (현재)
+++ hooks/log-reflection.sh (제안)
@@ 카테고리 정의
- misunderstanding: 사용자 의도를 잘못 해석
+ misunderstanding: 사용자 의도를 잘못 해석 (사용자가 명시한 대상/범위를 Claude가 다른 것으로 치환)
- wrong_approach: 더 적절한 스킬/에이전트/MCP 가 있었는데 비효율적으로 시도
+ wrong_approach: 의도는 맞게 파악했으나 선택한 도구/절차가 부적합
```

### (5) 다음 단계

- demote 후보 N개 → `/reflect-promote action=rollback rule_id=<id>` 개별 실행 권장
- 등급 상향 후보 M개 → `/reflect-promote` §B 실행 권장 (surface 이동 + ledger 대체 엔트리)
- 프롬프트 개선 적용 여부 (Y/N)
- 다음 kaizen 실행 예정일: `<date + 30d>`

## 안티패턴 (하지 말 것)

- LLM-as-judge 를 codex 같은 모델로 다시 돌리지 마라 (self-consistency 로 간주).
- **judge 재분류 프롬프트에 기존 태그 어휘를 주입하지 마라** — 일치도가 인위적으로 올라간다.
- `post_freq == 0` 하나로 demote 결정하지 마라 — `risk_class == low` 조건 필수.
- **파편화 임계 초과 상태에서 demote 후보를 내지 마라** — 그 `post_freq == 0` 은 "효과 있음" 이 아니라 "못 셌음" 이다.
- **`fold_ratio` 로 파편화를 판정하지 마라** — 아무것도 못 묶으면 1.00 이라 영원히 "정상" 이다.
- **재발이 늘어난 hook/CLAUDE.md 규칙에 등급 상향을 제안하지 마라** — 먼저 `hook-coverage-audit` 이다.
- **`post_freq` 를 `canonical_tag` 단독으로 세지 마라** — `aliases` 합산 필수. 과소집계는 효과 없는 규칙을 살려둔다.
- **재발한 규칙에 "문구를 더 강하게 쓰자" 는 제안을 내지 마라** — 등급 상향(`enforcement-escalation`)이거나, 올리지 않는 근거를 대라.
- **E1/E2/E3 를 이 문서에서 재정의하지 마라** — `harness/docs/guides/skill-design-guide.md` §3.7 이 정본.
- 임계값 변경을 1회 kaizen 만으로 확정하지 마라 — 최소 2개월 데이터 축적 후.
- `log-reflection.sh` 프롬프트를 자동 patch 하지 마라. diff 제안 + 사용자 승인.
- **`.env-issues.tsv` 를 삭제하거나 초기화하지 마라** — 환경 이슈의 유일한 누적 근거다. Stop 훅이 억제한 사건은 reflections 본문에 없다.
- harness-kaizen / contract-kaizen / evaluator-kaizen 의 이슈를 이 리포트에 섞지 마라.

## 예시 사용

- `/reflect-kaizen` — 현재 프로젝트, 30일 창, 10건 샘플
- `/reflect-kaizen window=60d sample=20` — 확장 측정
- `/reflect-kaizen project=claude-plugins-1a3bcba6`

## 관련 문서

- `reflect-kit/docs/DESIGN.md` — Precedence Table + 임계값 hypothesis 원본
- `reflect-kit/docs/SCHEMA.md` — ledger post_freq / status 필드 의미
- `reflect-kit/docs/RESEARCH.md` — LLM-as-judge 근거 리서치
- `reflect-kit/references/tag-canonicalization.md` — 파편화 지표·canonical/alias/family 규약 SSOT
- `reflect-kit/hooks/_lib-tag-canon.sh` — `tag_canon_fragmentation` / `tag_canon_groups` 실행 구현
- `reflect-kit/hooks/log-reflection.sh` — 프롬프트 개선 대상
