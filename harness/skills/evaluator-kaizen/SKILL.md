---
name: evaluator-kaizen
description: >
  qa-evaluator 에이전트를 학술 논문·공식 문서·커뮤니티 리서치·글로벌 피드백 기반으로 점진적으로 개선하는 카이젠 스킬.
  평가 방법론 가이드(qa-evaluation-guide)도 개선 대상에 포함.
  오케스트레이터 Phase 3으로 자동 호출, 피드백 임계치 이벤트 트리거, 또는 수동 호출로 동작한다.
  "/evaluator-kaizen", "평가자 카이젠", "evaluator 개선" 요청에 사용.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: "[skills|guide]"
user-invocable: true
---

# Evaluator Kaizen

qa-evaluator의 평가 품질을 리서치 + 실행 피드백 기반으로 점진적으로 개선한다.

## 이 스킬 폴더의 파일

- `references/search-sources.md` — 검색 소스 + 신뢰도 기준 (평가 방법론 12개 + 자기개선 6개 도메인)
- `references/pr-template.md` — PR 본문 + changelog 템플릿
- `scripts/trigger-check.sh` — 피드백 기반 이벤트 트리거 감지
- `templates/research-log-entry.md` — 연구 로그 엔트리 형식

## Gotchas

- 피드백이 0건이면 triage에서 SKIP하지 마라. 리서치 전용 모드로 진행한다 (패턴 분석 생략, search-sources.md 우선순위 상위 3개 도메인만 리서치).
- 리서치 도메인 전체(18개)를 한 번에 검색하지 마라. 피드백 패턴 분석 결과에서 3-5개만 선정한다. 피드백 0건이면 search-sources.md 우선순위 상위 3개만.
- WebFetch로 URL 접근 시 arXiv PDF 직접 접근은 실패할 수 있다. `arxiv.org/abs/` (abstract 페이지)를 사용해라.
- Phase 2(contract-kaizen)에서 contract-schema.md가 변경되었는지 확인해라. 변경 시 평가 루브릭에 새 필드 반영 필수.
- Draft → QA → Apply 순서를 지켜라. 개선안을 파일에 적용하기 전에 QA Evaluator가 DRAFT를 평가해야 한다.
- qa-evaluator 자체를 개선하는 Phase에서 QA는 **현재(구) 버전** evaluator로 수행한다. 개선된 버전으로 자기 자신을 QA하지 마라.
- Regression Smoke Test가 FAIL이면 git revert하고 BLOCKED로 기록한다. 연속 2회 FAIL이면 Phase를 중단하고 사용자에게 알린다.

## 개선 대상

| 영역 | 대상 파일 | 인자 필터 |
|------|----------|----------|
| 가이드 | `../../docs/guides/qa-evaluation-guide.md` | `guide` |
| 에이전트 프롬프트 | `harness/agents/qa-evaluator.md` | `skills` |

## 트리거 조건

| 트리거 | 조건 |
|--------|------|
| 오케스트레이터 | Phase 3으로 자동 호출 |
| 피드백 임계치 | 최근 피드백 10건 중 동일 진단 항목 3회 이상 반복 |
| 수동 | `/evaluator-kaizen`, `/evaluator-kaizen guide`, `/evaluator-kaizen skills` |

## Process

### Step 1: 상태 확인

1. `docs/kaizen/research-log.md`에서 마지막 evaluator-kaizen 엔트리 확인
2. 트리거 사유 파악
3. 현재 qa-evaluator.md + qa-evaluation-guide.md 상태 스캔
4. `harness/references/contract-schema.md` 최근 변경 여부 확인 (Phase 2에서 변경되었을 수 있음)

### Step 2: Triage (피드백 분석)

1. `bash harness/scripts/feedback-path.sh`로 글로벌 피드백 경로 확인
2. `evaluator/` 하위 YAML 파일 읽기
3. 패턴 분석:
   - L3 미도달 빈도 (l3_coverage가 일관되게 낮은 패턴)
   - REJECT 반복 패턴 (동일 reject_reasons)
   - False APPROVE 징후 (APPROVE 후 관련 영역에서 버그 보고)
   - 편향 감지 빈도
   - 교차 진단에서 반복 지적되는 문제
4. 피드백이 0건이면 패턴 분석 생략 → 리서치 전용 모드로 Step 3 진행
5. 피드백이 있지만 개선 포인트가 없으면 SKIP + 로그 기록 후 종료

### Step 3: COLLECT (리서치)

1. `references/search-sources.md` 읽기
2. 피드백 패턴에서 식별된 문제 영역 → 관련 도메인 3-5개 선정
   - 피드백 0건이면: 우선순위 상위 3개 (LLM-as-a-Judge, Rubric-Based Evaluation, Test Oracle Problem)
3. contract-schema.md 변경이 있으면: 해당 변경에 관련된 도메인 우선 추가
4. 선정된 도메인별 WebSearch 실행
5. 결과 URL 수집

### Step 4: VERIFY (3-gate 검증)

| Gate | 검증 | 실패 시 |
|------|------|---------|
| GATE 1 | 모든 주장에 URL이 있는가? | URL 없는 주장 폐기 |
| GATE 2 | WebFetch로 URL 접근 + 내용 일치? | 접근 불가 URL 폐기 |
| GATE 3 | PR에 출처 URL + 인용 포함? | PR 작성 시 강제 |

### Step 5: GAP 분석 + 예방적 분석

1. **GAP 분석**: 리서치 결과 + 피드백 패턴 + 현재 qa-evaluator.md + qa-evaluation-guide.md 대조
2. **예방적 분석**: 리서치 anti-pattern을 현재 에이전트 프롬프트에 대조
3. **스키마 변경 반영**: contract-schema.md에 새 필드가 추가되었으면 평가 루브릭에 반영 포인트 추가
4. 개선점 목록 작성

### Step 6: Sprint Contract (DRAFT) + 개선안 작성

1. 현재 버전의 sprint-contract로 Sprint Contract 작성
2. 개선안을 DRAFT로 작성 — **파일에 적용하지 않는다**
3. DRAFT를 대화에 출력하여 QA 대상으로 제시

### Step 7: QA + 적용 + Regression

1. **현재(구) 버전**의 qa-evaluator로 DRAFT 평가
2. APPROVE:
   - `kaizen-phase-3-pre` git tag 생성
   - 파일에 적용 + 커밋
   - Regression Smoke Test (`harness/evals/kaizen/evaluator-kaizen/` 활용)
   - Regression PASS → 완료
   - Regression FAIL → `git revert` + BLOCKED
3. REJECT: 피드백 반영 → 재QA (최대 3회) → 3회 시 에스컬레이션

### Step 8: 기록

1. `docs/kaizen/research-log.md`에 엔트리 추가
2. `docs/kaizen/changelog.md`에 변경 기록
3. 버전 bump 판단

## 버전 bump 판단 가이드

| 변경 유형 | bump |
|-----------|------|
| qa-evaluation-guide.md만 수정 | patch |
| Gotchas 추가/수정 | patch |
| 검증 레벨/루브릭 변경 | minor |
| 판정 로직 구조 변경 | major |

## References

- `../../docs/guides/qa-evaluation-guide.md` — 평가 방법론 가이드
- `harness/agents/qa-evaluator.md` — 개선 대상 에이전트
- `harness/references/contract-schema.md` — 계약 스키마 (Phase 2 변경 감지용)
- `harness/references/feedback-schema.yaml` — 피드백 YAML 스키마
- `docs/kaizen/research-log.md` — 연구 로그
- `docs/kaizen/changelog.md` — 변경 이력
