---
name: harness-kaizen
description: >
  하네스 엔지니어링을 학술 논문·공식 문서·커뮤니티 리서치 기반으로
  점진적으로 개선하는 카이젠 스킬.
  주 1회 cron 자동 실행, 이벤트 트리거(REJECT 연속, anti-pattern 반복,
  신규 스킬 추가), 또는 수동 호출로 동작한다.
  "/harness-kaizen", "하네스 개선", "카이젠" 요청에 사용.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: "[config|skills|guide]"
user-invocable: true
---

# Harness Kaizen

하네스 프레임워크를 최신 연구와 실무 기법에 맞춰 점진적으로 개선한다.
연구 결과는 PR로 제출하여 사용자가 리뷰 후 머지한다.

## 이 스킬 폴더의 파일

필요할 때 읽어라:

- `references/search-sources.md` — 검색 소스 목록 + 신뢰도 기준
- `references/pr-template.md` — PR 본문 + changelog 엔트리 템플릿
- `scripts/trigger-check.sh` — 이벤트 트리거 감지 스크립트
- `templates/research-log-entry.md` — 연구 로그 엔트리 형식

## Gotchas

- WebFetch 로 URL 접근 시 arXiv PDF 직접 접근은 실패할 수 있다. `arxiv.org/abs/` (abstract 페이지) 를 사용해라
- GitHub trending 은 페이지 구조가 자주 바뀐다. WebSearch 로 "github trending {키워드}" 를 검색하는 게 더 안정적이다
- Anthropic docs changelog 는 단일 URL 이 없을 수 있다. WebSearch 로 "anthropic docs changelog site:docs.anthropic.com" 검색해라
- 논문 제목만으로 검색하면 동명 논문이 나올 수 있다. 반드시 저자명 또는 arXiv ID 를 함께 확인해라
- `release.sh` 는 interactive prompt 가 있다 (dirty check). 카이젠 브랜치에서는 커밋 후 실행해야 한다
- **피드백 0 건이면 triage 에서 SKIP 하지 마라** — contract-kaizen / evaluator-kaizen 과 동일하게 **리서치 전용 모드** 로 진행한다 (패턴 분석 생략, `references/search-sources.md` 우선순위 상위 3 개 도메인만 리서치). 피드백 누적이 없어도 2026 트렌드 리서치 기반 예방적 개선은 항상 가능하다 (리서치 근거: GrowthBook "Feedback Loops are the Next Breakthrough in Agentic Coding", Martin Fowler "Humans and Agents in Software Engineering Loops")
- 피드백 패턴 분석 시 동일 `diagnosis.checklist` 시그니처가 **최근 10 건 중 3 회 이상** 반복되면 해당 영역을 최우선 개선 대상으로 승격시켜라. 이는 contract-kaizen / evaluator-kaizen 의 임계치와 일치시켜 일관성을 유지한다
- **Scope Creep 방지** — 한 카이젠 사이클에서 개선하는 파일은 최대 3개로 제한해라. 4개 이상을 한 번에 수정하면 Regression Smoke Test에서 원인 특정이 불가능해지고 revert 범위가 넓어진다. 큰 개선은 여러 사이클로 분할한다.
- **Cross-Phase 오염 금지** — harness-kaizen Phase에서 contract-schema.md나 qa-evaluation-guide.md를 직접 수정하지 마라. 그것은 contract-kaizen(Phase 2)과 evaluator-kaizen(Phase 3)의 전담 영역이다. harness-kaizen에서 발견한 교차 이슈는 "DEFERRED to phase-N" 주석으로 기록만 하고 해당 Phase에 위임한다.
- **Regression 원인 추적 누락** — Smoke Test FAIL 시 단순 revert만 하고 끝내면 같은 패턴의 실패가 반복된다. revert 후 반드시 "왜 실패했는가"를 1줄로 기록하고 다음 사이클의 피드백 입력으로 활용해라.

## 핵심 제약: 할루시네이션 절대 불가

**출처 없는 주장은 어떤 경우에도 반영하지 않는다.**

3중 검증 게이트를 반드시 통과해야 한다:
1. **GATE 1 — 출처 존재:** 모든 주장에 URL 필수. 없으면 즉시 폐기
2. **GATE 2 — 출처 접근:** WebFetch로 URL 접근 + 내용이 주장과 일치하는지 확인. 실패 시 폐기
3. **GATE 3 — 증거 첨부:** PR에 출처 URL + 인용 원문 포함. 사용자가 원문 대조 가능해야 함

**추가 안전장치:**
- arXiv preprint → `[preprint]` 태그
- 블로그 → 작성자 신뢰도 표기 (공식 vs 개인)
- 6개월 이상 된 정보 → `[dated: YYYY-MM]` 태그

**이 게이트를 우회하고 싶은 생각이 들면 멈춰라:**
- "이건 널리 알려진 사실이니 출처 없어도 된다" → 아니다. 출처를 찾아라
- "URL은 안 되지만 내용은 맞다" → 검증 불가능하면 폐기다
- "비슷한 내용의 다른 출처가 있으니 괜찮다" → 그 다른 출처를 사용해라

## 개선 대상 범위

| 영역 | 대상 | 인수 필터 |
|------|------|-----------|
| 하네스 설정 | `.harness/project.yaml`, `procedures/` | `config` |
| 스킬 프롬프트 | `harness/skills/*/SKILL.md` | `skills` |
| 에이전트 로직 | `harness/agents/qa-evaluator.md` | `skills` |
| Eval | `harness/evals/` | `skills` |
| 아키텍처 | `harness/` 전체 구조, 훅, 스크립트 | `config` |
| 스킬 설계 가이드 | `../../docs/guides/skill-design-guide.md` | `guide` |
| 에이전트 설계 가이드 | `../../docs/guides/agent-design-guide.md` | `guide` |
| 피드백 스키마 | `../../references/feedback-schema.yaml` | `config` |

`$ARGUMENTS`가 없으면 전체 영역을 스캔한다.

## 트리거 조건

### 주기적 (cron)
- **직접 cron 없음** — `kaizen-orchestrator`가 Phase 2에서 호출
- 독립 실행은 수동 호출로만

### 이벤트 트리거
`scripts/trigger-check.sh`를 실행하여 감지:
- QA Evaluator REJECT 2회 연속
- 같은 anti-pattern 3회 이상 반복
- 신규 스킬 추가 후 첫 주

### 수동
- `/harness-kaizen` — 전체
- `/harness-kaizen config` — 설정만
- `/harness-kaizen skills` — 스킬만
- `/harness-kaizen guide` — 설계 가이드만

## Process

### Step 1: 상태 확인

1. `docs/kaizen/research-log.md`를 읽어 이전 연구 기록 확인
2. 이벤트 트리거 실행 시: 트리거 사유를 기록
3. 현재 하네스 상태 스캔:
   - `.harness/project.yaml` 읽기
   - `harness/skills/` 내 모든 SKILL.md 목록 확인
   - `harness/agents/qa-evaluator.md` 읽기
   - `../../docs/guides/skill-design-guide.md` 읽기
   - `../../docs/guides/agent-design-guide.md` 읽기
   - `harness/.claude-plugin/plugin.json`에서 현재 버전 확인

### Step 2a: Triage (피드백 패턴 분석)

2026 agentic regression detection 트렌드 (Sauce Labs, ContextQA, GrowthBook) 에 맞춰 COLLECT 전에 글로벌 피드백을 먼저 분석한다. contract-kaizen / evaluator-kaizen 과 동일한 Triage 프로토콜을 공유한다.

1. `bash harness/scripts/feedback-path.sh` 로 글로벌 피드백 경로 확인
2. `contract/` 와 `evaluator/` 하위 YAML 파일 읽기 (최근 10 건)
3. 패턴 분석:
   - 반복 실패 패턴 — 동일 `diagnosis.checklist` 시그니처 빈도 (최근 10 건 중 3 회 이상 = 임계치 초과)
   - optional 필드 활용 — `repeat_count` 가 2 이상인 피드백 우선 검토
   - `regression_link` 가 non-null 인 피드백 — APPROVE 후 재발한 회귀 이슈 (최우선 개선)
   - 카테고리 편중 — `category_coverage` 가 일관되게 낮은 영역
   - 교차 진단에서 반복 지적되는 문제 (`cross_diagnosis_notes`)
4. 피드백이 0 건이면 패턴 분석 생략 → **리서치 전용 모드** 로 Step 2b 진행 (Gotchas 참조)
5. 임계치 초과 항목이 있으면 Step 2b 리서치 도메인 선정 시 해당 영역 우선

### Step 2b: COLLECT (수집)

`references/search-sources.md`를 읽고 소스별로 검색한다.

**검색 실행:**
1. **WebSearch**로 학술 논문 검색 — 키워드 조합 사용
2. **WebSearch**로 공식 소스 changelog/blog 검색
3. **WebSearch**로 커뮤니티 소스 검색
4. 이전 research-log.md에 있는 URL은 건너뛴다 (업데이트 제외)

**각 검색 결과마다:**
- 제목, URL, 유형, 날짜를 기록
- 하네스 개선과 관련 있는지 1차 판단

### Step 3: VERIFY (검증)

수집한 각 소스에 대해 3중 검증 게이트를 실행한다.

**GATE 1:** URL이 있는가? → 없으면 폐기
**GATE 2:** WebFetch로 URL 접근 → 접근 불가면 폐기 → 내용이 주장과 일치하는지 확인 → 불일치면 폐기
**GATE 3:** 검증 통과한 소스만 다음 단계로

**태그 부착:**
- arXiv preprint → `[preprint]`
- 공식이 아닌 블로그 → `[blog]`
- 6개월 이상 → `[dated: YYYY-MM]`

### Step 4: ANALYZE (분석)

검증된 소스에서 추출한 인사이트와 현재 하네스 상태를 비교한다.

**갭 분석:**
- 현재 하네스에 없는 기법/패턴이 있는가?
- 현재 방식보다 나은 접근법이 제시되었는가?
- 설계 가이드에 추가할 새 원칙이 있는가?

**개선 포인트 도출:**
- 각 포인트에 영역(config/skill/agent/eval/architecture/guide) 태그
- 영향도(높음/중간/낮음)와 리스크(높음/중간/낮음) 판단
- 출처 URL과 구체적 근거 매핑

**개선 포인트가 없으면:** research-log.md에 "개선 포인트 없음"으로 기록하고 종료.

### Step 5: PROPOSE + APPLY (제안 및 적용)

1. **브랜치 생성:**
   - 버전 결정: 개선 항목 중 가장 높은 bump 유형 선택
     - docs, config 튜닝, Gotchas 추가 → patch
     - 스킬 프롬프트 변경, eval 기준 변경, 새 procedure → minor
     - 아키텍처 변경, 에이전트 로직 대폭 수정 → major
   - 새 버전 계산
   - 브랜치명: `kaizen/{새버전}-{YYYY-MM-DD}`

   ```bash
   git checkout -b kaizen/{새버전}-{YYYY-MM-DD}
   ```

2. **변경 적용:**
   - 각 개선 포인트에 해당하는 파일을 수정
   - 변경마다 커밋: `kaizen: {변경 설명}`

3. **버전 업데이트:**
   - `harness/.claude-plugin/plugin.json`의 version 필드 업데이트
   - `.claude-plugin/marketplace.json`의 description에서 `[vX.Y.Z · 날짜]` 업데이트
   - `docs/kaizen/changelog.md`에 엔트리 추가 (`references/pr-template.md`의 changelog 형식 따름)

4. **research-log.md 업데이트:**
   - `templates/research-log-entry.md` 형식으로 이번 연구 결과 기록

5. **README 업데이트:**
   - `harness/README.md`의 카이젠 섹션에 이번 개선 사항 반영
   - 변경된 기능, 새로 추가된 원칙, 버전 정보를 최신 상태로 유지

6. **PR 생성:**
   - `references/pr-template.md`를 읽고 해당 형식으로 PR 본문 작성
   - PR 제목: `[{bump유형}] {핵심 변경 요약}`

   ```bash
   git push -u origin kaizen/{새버전}-{YYYY-MM-DD}
   gh pr create --title "[{bump}] {요약}" --body "{pr-template.md 형식에 맞춘 본문}"
   ```

7. **git tag는 PR 머지 후** 사용자가 `/release`로 처리한다. 카이젠은 tag를 생성하지 않는다.

## 버전 판단 가이드

| 변경 영역 | bump | 예시 |
|-----------|------|------|
| docs, config 튜닝, anti-pattern 추가, Gotchas 추가 | **patch** | project.yaml에 anti-pattern 1개 추가 |
| 스킬 프롬프트 변경, eval 기준 변경, 새 procedure 추가 | **minor** | sprint-contract 스킬의 프로세스 단계 수정 |
| 아키텍처 변경, 에이전트 로직 대폭 수정, breaking change | **major** | qa-evaluator 평가 방식 전면 교체 |

**혼합 변경 시:** 가장 높은 bump 유형을 따른다 (config patch + skill minor = minor).

## 추적 규칙

| 항목 | 규칙 | 예시 |
|------|------|------|
| 커밋 메시지 | `kaizen:` prefix | `kaizen: sprint-contract few-shot 판단 로직 추가` |
| 브랜치명 | 버전 + 날짜 | `kaizen/0.4.0-2026-04-07` |
| PR 제목 | bump 유형 명시 | `[minor] sprint-contract 복잡도 판단 개선` |

## Step 6: Plugin Validation 결과 반영

카이젠 세션 시작/종료 시 `scripts/validate-plugin.py harness` 를 실행하여 7 카테고리 상태를 확인하고 결과를 개선 우선순위에 반영한다.

**실행 패턴, 우선순위 매핑, 통합 규칙**은 `harness/docs/guides/plugin-validation-guide.md §7` 에서 정의한다 (SSOT) — 해당 섹션을 그대로 따른다.

## References

- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 7 카테고리 기준 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
