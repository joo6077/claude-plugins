---
feature: "kaizen Phase 2 — Contract (contract-design-guide · sprint-contract · contract-schema) enforcement 승급 + Counterpart 흡수"
created: "2026-07-27 18:56"
complexity: "복잡"
conditions: 16
---

# Sprint Contract — Phase 2 Contract 카이젠

## 배경 · 이번 사이클 프레이밍

`/insights` 2026-07-27 의 Friction #1·#3 은 직전 사이클 승격분인데 세션당 비율이 줄지 않았다.
따라서 이번 Phase 2 도 **새 soft 문장을 추가하는 것이 아니라 기존 규칙의 enforcement 등급을
올리는 것**이 정답이다 (Phase 1 §3.7 등급 사다리 준용).

흡수 대상은 세 갈래로 한정한다:

1. **Phase 1 이 넘긴 숙제** — Counterpart Enumeration 을 evaluator 가이드가 아니라 **계약 조건**
   으로 흡수한다 (skill-design-guide §11 parity item 12 설계).
2. **digest 가 지목한 sprint-contract 실사용 결함 5 종** — 4 종은 이미 규칙이 있는데 재위반이므로
   등급 승급, 1 종(cwd 드리프트)만 신규.
3. **글로벌 REJECT 89 건에서 반복되는 계약 품질 결함 4 종** — diff oracle 모호 / preamble 모순 /
   `[exact]` 산출물 오분류 / 증거 아티팩트 부재.

용어는 Phase 1 이 정한 `[미검증]` · `E1`/`E2`/`E3` 를 그대로 쓴다. 신규 용어를 만들지 않는다.

## 리서치 소스 (필수 3+ 건 · 실제 5 건 조회)

Context7 MCP 는 이 세션에서 OAuth 미인증이라 사용 불가 → `phase-research-templates.md` §Phase 2 의
fallback 인 WebFetch/WebSearch 로 1 차 출처를 직접 조회했다.

| # | 소스 | 유형 | URL |
| - | ---- | ---- | --- |
| 1 | LLMs-as-Judges Survey (criteria 분해 · 판정 비이행성) | 학술 | <https://arxiv.org/html/2412.05579v2> |
| 2 | Gherkin Best Practices (one When-Then pair · declarative) | community | <https://github.com/andredesousa/gherkin-best-practices> |
| 3 | Pact — Contract tests are not functional tests (양면 검증 · 과잉 계약 경고) | 공식 | <https://docs.pact.io/consumer/contract_tests_not_functional_tests> |
| 4 | Pact — What is Pact good for (공유 아티팩트로서의 계약) | 공식 | <https://docs.pact.io/getting_started/what_is_pact_good_for> |
| 5 | AI Spec Template (spec oracle · Not-Included 절 · 지시 충돌의 조용한 해소) | community | <https://www.augmentcode.com/guides/ai-spec-template> |

## GAP 분석 (리서치·실측 데이터 vs 현재 계약 레이어)

| # | 신호 | 근거 | 현재 상태 | 판정 |
| - | ---- | ---- | --------- | ---- |
| G1 | 양면(producer/consumer) 미열거 | insights Friction #4 · 소스 3·4 (양쪽을 다 검증해야 통합 실패가 잡힌다) | contract-design-guide 에 반대편 열거 원칙 없음. Phase 1 이 "계약 조건으로 흡수" 를 명시 위임 | 신규 절 + 조건 패턴 (E2) |
| G2 | Pre-Edit Audit 재위반 | digest `skipped-pre-edit-audit` (usc=true) | SKILL.md Gotcha 문장(E1)만 존재 · Process 단계 없음 | **E1 → E2 승급** |
| G3 | project.yaml 명령 리터럴 불일치 | digest `config-command-mismatch` + `ignored-project-commands` (2 건) | Gotcha 는 "config 에서 읽어라" 까지. 리터럴 전사 요구 없음 | **E1 → E2 승급** (대조표) |
| G4 | 파서 비호환 섹션 | digest `parser-incompatible-contract-section` (usc=true) | SKILL.md 는 조건 섹션만 허용한다고 서술하나, 실제 카이젠 계약은 배경·리서치·GAP·범위 섹션을 상시 사용 → **규칙이 실제와 어긋나 재위반** | 스키마에 헤더 2 계층 분류 + **E3 인라인 게이트** |
| G5 | 복잡도를 파일 수로 판정 | digest `complexity-by-file-count` (usc=true) | Gotcha 1 행 + 안티패턴 1 행 (둘 다 E1) | **E1 → E2 승급** (판정 표) |
| G6 | cwd 계약 경로 드리프트 | digest `cwd-contract-path-drift` | 규칙 없음 | 신규 E1 (CONTRACT_ROOT 고정) |
| G7 | diff scope oracle 모호 (3 회 재발) | REJECT AR-01 (2026-06-11) · AR-01 (2026-06-29, 미커밋 `*.g.dart` 혼입) · Improvement (2026-07-21, `git diff --cached` 권고) | §측정 명령 타당성 이 커밋 전제는 다루나 (a) staged vs working tree 선택 (b) 생성물 제외 pathspec 이 없음 | **E1 → E3 승급** (표준형 강제) |
| G8 | preamble–조건 모순 | REJECT RE-02 (2026-07-22) + Improvement 2 건 · 소스 5 ("지시가 충돌하면 에이전트가 조용히 한쪽을 고른다") | 원칙 없음 | 신규 절 (E2) |
| G9 | `[exact]` 산출물 오분류 | REJECT UI-07 + Improvement 2 건 (2026-07-13) | 태그 선택 기준에 "산출물 동반 제출" 규칙 없음 | 태그 기준 보강 |
| G10 | goal 조건의 증거 아티팩트 부재 | REJECT UI-06 (2026-07-13, 시안 승인 기록 없음) | 검증 수단 명시 의무는 "측정 방법" 만 요구 · 증거가 **존재할 경로** 요구 없음 | 신규 소절 (E2) |

**예방적 분석 — 리서치가 경고하는 반패턴의 잔존 여부**

- 소스 3 "over-specified contract": Counterpart 조건이 소비면 **내부 로직**까지 요구하면 과잉 계약이
  되어 정상 변경을 위반으로 만든다 → 신규 절에서 열거 대상을 **파일 경로 + 관찰 가능한 동작**으로
  한정하고 소비면 구현 상세 조건화를 금지 문구로 박는다.
- 소스 2 "one When-Then pair": Counterpart 조건을 producer/consumer 한 줄에 묶으면 복합 조건이 된다
  → 양면을 **별도 조건 2 개**로 분리하도록 규정한다.
- 소스 5 "Not Included 절": 범위 밖 선언이 없으면 에이전트가 인접 기능을 추가한다 → 본 계약 자체에
  범위 경계 절을 유지한다 (기존 관례 보존, 신규 규칙 아님).
- 소스 1 "판정 비이행성": 조건은 pointwise binary 로 유지 — 비교형("A 가 B 보다 낫다") 조건을
  이번 개정에서 도입하지 않는다.

## Skill

- [ ] SK-01: `harness/skills/sprint-contract/SKILL.md` Process 에 `CONTRACT_ROOT` (= `.harness/project.yaml` 을 발견한 디렉토리의 절대경로) 를 확정하고 이후 모든 계약 경로를 그 기준으로 쓰라는 요구가 존재한다 [exact] · 측정: `grep -c "CONTRACT_ROOT" harness/skills/sprint-contract/SKILL.md` 결과 ≥ 2
- [ ] SK-02: DRAFT 제시 **전** 에 "설정 리터럴 대조표"(config key → project.yaml 에서 읽은 값 → 계약에 쓴 값) 를 출력하도록 요구하는 E2 아티팩트 단계가 Process 에 존재하고, 값을 **리터럴 그대로** 전사하라는 문구가 포함된다 [structural] · 측정: Read 로 Process 확인 (`config-command-mismatch` 직접 대응)
- [ ] SK-03: Pre-Edit Audit 이 Gotcha 문장에서 **Process 필수 단계**로 승급되고, 감사한 대상 파일의 경로를 `파일:라인` 형태 증거로 표에 남기도록 요구한다 [structural] · 측정: Read — Process 에 단계 번호가 부여되어 있어야 PASS (Gotcha 문장만 남으면 FAIL)
- [ ] SK-04: 복잡도 판정을 파일 수가 아닌 영향 범위 4 축(레이어 수 / 공개 API·계약 변경 여부 / 소비면 존재 여부 / 회귀 위험)으로 표에 기록하도록 Process 에 명시된다 [exact, enumerated] · 측정: Read — 4 축이 모두 문자로 등장해야 PASS
- [ ] SK-05: 계약 저장 직후 헤더·조건 배치를 검사하는 **결정론적 인라인 게이트**(LLM 판단 없이 grep 계열 명령 1 개 이상)와 "위반 시 다음 단계 진행 금지" 문구가 Process 에 존재한다 [structural] · 측정: Read (`parser-incompatible-contract-section` 직접 대응)
- [ ] SK-06: Process 에 Counterpart 조건 삽입 단계가 존재하고, 계약·직렬화·공유 모델 변경 시 producer/consumer 조건을 **각각 별도 조건**으로 쓰라는 요구가 포함된다 [structural] · 측정: `grep -n "Counterpart" harness/skills/sprint-contract/SKILL.md`

## Script

- [ ] SC-01: 이번 Phase 의 `harness/` 하위 변경 파일이 정확히 3 개다 [exact, enumerated] · Given: 커밋 직전 working tree · 측정: `git diff --name-only HEAD -- harness/` 결과가 `harness/docs/guides/contract-design-guide.md`, `harness/references/contract-schema.md`, `harness/skills/sprint-contract/SKILL.md` 3 행과 정확히 일치
- [ ] SC-02: Phase 3 소관 파일 변경 0 건 [exact] · Given: 커밋 직전 working tree · 측정: `git diff --name-only HEAD -- harness/agents/qa-evaluator.md harness/docs/guides/qa-evaluation-guide.md` 결과 0 행

## Error

- [ ] ER-01: 신설·개정된 원칙 6 건(Counterpart 조건화 / diff-scope oracle 표준형 / preamble–조건 정합 / `[exact]` 산출물 규칙 / 증거 아티팩트 존재 의무 / 헤더 2 계층 분류) 각각에 실제 발생 사례(글로벌 REJECT ID 또는 digest mistake_tag)가 근거로 인용된다 [structural, enumerated] · 측정: contract-design-guide 각 절 Read — 근거 없는 절이 1 건이라도 있으면 FAIL
- [ ] ER-02: contract-design-guide 에 계약 원칙별 enforcement 등급(E1/E2/E3) 표가 존재하고, 재발 이력으로 **승급**된 규칙 4 건(Pre-Edit Audit / 설정 리터럴 / diff-scope oracle / 복잡도 판정)이 표에 승급 근거와 함께 기록된다 [exact, enumerated] · 측정: 등급 표 Read

## Architecture

- [ ] AR-01: `harness/references/contract-schema.md` 스키마 버전이 v3 → **v4** 로 bump 되고 변경 이력에 v4 항목이 추가된다 [exact] · 측정: `grep -n "현재: \*\*v4\*\*" harness/references/contract-schema.md` 1 행 이상
- [ ] AR-02: 신규 용어 0 건 — `[미검증]`, `E1`/`E2`/`E3` 를 Phase 1 정의 그대로 사용하고 동의어(예: `UNVERIFIED`, `등급 A/B/C`) 를 만들지 않는다 [exact] · 측정: `grep -n "UNVERIFIED\|미확인\|등급 A" harness/docs/guides/contract-design-guide.md harness/skills/sprint-contract/SKILL.md harness/references/contract-schema.md` 결과 0 행
- [ ] AR-03: contract-design-guide 의 parity 표에 Counterpart Enumeration 이 skill-design-guide §5.5 대응(parity item 12) 위치로 1 행 추가된다 [exact] · 측정: parity 표 Read
- [ ] AR-04: 세 파일이 서로 모순되지 않는다 — (a) 허용 섹션 헤더 2 계층 분류 (b) diff-scope oracle 표준형 (c) Counterpart 조건 표기가 3 파일에서 동일 어휘로 기술된다 [exact, enumerated] · 측정: 3 파일 교차 Read
- [ ] AR-05: contract-design-guide 머리말의 "최근 갱신" 블록과 문서 말미 §버전 정보가 **동시에** v4 로 갱신된다 [exact] · 측정: `head -20` + `tail -10` — 한쪽만 갱신되면 FAIL

## Anti-patterns

- [ ] AP-03: `^```\s*$` — bare code fence 금지. 신규/수정 fence 전부 언어 태그 필수 (`text`, `bash`, `yaml`, `markdown`)
- [ ] AP-04: SKILL.md frontmatter 의 `name` 필드 손상 금지 — validate-plugin V1 FAIL 방지

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 본 Phase 에서는 신규 원칙을 sprint-contract 전용 문구로 가두지 않고 contract-design-guide(공용 가이드)에 정의하고 SKILL.md 가 참조한다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — Phase 1 이 정의한 `[미검증]` · E1/E2/E3 규약을 재사용하고 계약 레이어 전용 용어를 신설하지 않는다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상 — 본 Phase 는 `.md` 3 파일만 변경하므로 무영향임을 실행으로 확인)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude: []` — 제외 항목 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 본 레포는 구동 대상 앱/서버가 없으므로 회귀 게이트 `python3 scripts/validate-plugin.py` 로 대체 측정 (11 plugins 전부 OK · Exit 0)

## 범위 경계

**변경 허용**: `harness/docs/guides/contract-design-guide.md`, `harness/skills/sprint-contract/SKILL.md`,
`harness/references/contract-schema.md`.

**변경 금지**: 그 외 전부 — 특히 `harness/agents/qa-evaluator.md` 와
`harness/docs/guides/qa-evaluation-guide.md` 는 **Phase 3 소관**. 다른 kit, `marketplace.json`,
`plugin.json`, changelog, README 도 금지. 브랜치 생성 / push / PR 금지 — 커밋까지만.
`.harness/sprint-contract.md` 와 `.harness/history/` 이동은 프로세스 산출물로 허용.

## 회귀 게이트

- `python3 scripts/validate-plugin.py` → 11 plugins 전부 OK · Exit 0
- `git diff --name-only HEAD -- harness/` 결과가 허용 3 파일로 한정
