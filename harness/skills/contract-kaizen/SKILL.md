---
name: contract-kaizen
description: >
  sprint-contract 스킬을 학술 논문·공식 문서·커뮤니티 리서치·글로벌 피드백 기반으로 점진적으로 개선하는 카이젠 스킬.
  계약 설계 원칙(contract-design-guide)과 계약 스키마(contract-schema)도 개선 대상에 포함.
  오케스트레이터 Phase 2로 자동 호출, 피드백 임계치 이벤트 트리거, 또는 수동 호출로 동작한다.
  "/contract-kaizen", "계약 카이젠", "contract 개선" 요청에 사용.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: "[config|skills|guide]"
user-invocable: true
---

# Contract Kaizen

sprint-contract의 계약 작성 품질을 리서치 + 실행 피드백 기반으로 점진적으로 개선한다.

## 이 스킬 폴더의 파일

- `references/search-sources.md` — 검색 소스 + 신뢰도 기준 (계약 설계 11개 + 자기개선 6개 도메인)
- `references/pr-template.md` — PR 본문 + changelog 템플릿
- `scripts/trigger-check.sh` — 피드백 기반 이벤트 트리거 감지
- `templates/research-log-entry.md` — 연구 로그 엔트리 형식

## Gotchas

- 피드백이 0건이면 triage에서 SKIP하지 마라. 리서치 전용 모드로 진행한다 (패턴 분석 생략, search-sources.md 우선순위 상위 3개 도메인만 리서치).
- 리서치 도메인 전체(17개)를 한 번에 검색하지 마라. 피드백 패턴 분석 결과에서 3-5개만 선정한다. 피드백 0건이면 search-sources.md 우선순위 상위 3개만.
- WebFetch로 URL 접근 시 arXiv PDF 직접 접근은 실패할 수 있다. `arxiv.org/abs/` (abstract 페이지)를 사용해라.
- contract-schema.md를 변경하면 evaluator-kaizen(Phase 3)에 영향을 준다. 스키마 변경은 반드시 PR 본문에 명시해라.
- Draft → QA → Apply 순서를 지켜라. 개선안을 파일에 적용하기 전에 QA Evaluator가 DRAFT를 평가해야 한다.
- Regression Smoke Test가 FAIL이면 git revert하고 BLOCKED로 기록한다. 연속 2회 FAIL이면 Phase를 중단하고 사용자에게 알린다.

## 개선 대상

| 영역 | 대상 파일 | 인자 필터 |
|------|----------|----------|
| 가이드 | `../../docs/guides/contract-design-guide.md` | `guide` |
| 스킬 프롬프트 | `harness/skills/sprint-contract/SKILL.md` | `skills` |
| 계약 스키마 | `harness/references/contract-schema.md` | `config` |

## 트리거 조건

| 트리거 | 조건 |
|--------|------|
| 오케스트레이터 | Phase 2로 자동 호출 |
| 피드백 임계치 | 최근 피드백 10건 중 동일 진단 항목 3회 이상 반복 |
| 수동 | `/contract-kaizen`, `/contract-kaizen guide`, `/contract-kaizen skills` |

## Process

### Step 1: 상태 확인

1. `docs/kaizen/research-log.md`에서 마지막 contract-kaizen 엔트리 확인
2. 트리거 사유 파악 (오케스트레이터 호출 / 피드백 임계치 / 수동)
3. 현재 sprint-contract SKILL.md + contract-design-guide.md 상태 스캔

### Step 2: Triage (피드백 분석)

1. `bash harness/scripts/feedback-path.sh`로 글로벌 피드백 경로 확인
2. `contract/` 하위 YAML 파일 읽기
3. 패턴 분석:
   - 반복 실패 패턴 (동일 diagnosis.checklist 항목이 true인 빈도)
   - 카테고리 편중 (category_coverage가 일관되게 낮은 영역)
   - 복잡도 과소평가 빈도
   - 교차 진단에서 반복 지적되는 문제
4. 피드백이 0건이면 패턴 분석 생략 → 리서치 전용 모드로 Step 3 진행
5. 피드백이 있지만 개선 포인트가 없으면 SKIP + `docs/kaizen/research-log.md`에 "개선 포인트 없음" 기록 후 종료

### Step 3: COLLECT (리서치)

1. `references/search-sources.md` 읽기
2. 피드백 패턴에서 식별된 문제 영역 → 관련 도메인 3-5개 선정
   - 피드백 0건이면: 우선순위 상위 3개 (BDD/Gherkin, Requirements Engineering, Design by Contract)
3. 선정된 도메인별 WebSearch 실행
4. 결과 URL 수집

### Step 4: VERIFY (3-gate 검증)

| Gate | 검증 | 실패 시 |
|------|------|---------|
| GATE 1 | 모든 주장에 URL이 있는가? | URL 없는 주장 폐기 |
| GATE 2 | WebFetch로 URL 접근 + 내용 일치? | 접근 불가 URL 폐기 |
| GATE 3 | PR에 출처 URL + 인용 포함? | PR 작성 시 강제 |

arXiv preprint은 `[preprint]`, 비공식 블로그는 `[blog]`, 6개월 이상은 `[dated: YYYY-MM]` 태그.

### Step 5: GAP 분석 + 예방적 분석

1. **GAP 분석**: 리서치 결과 + 피드백 패턴 + 현재 sprint-contract SKILL.md + contract-design-guide.md 대조
   - 리서치에서 권장하지만 현재 스킬에 없는 것
   - 피드백에서 반복되지만 Gotchas에 없는 패턴
2. **예방적 분석**: 리서치 anti-pattern을 현재 프롬프트에 대조
   - 아직 발생하지 않았지만 발생할 수 있는 취약점
3. 개선점 목록 작성 (가이드 개선 / 스킬 프롬프트 개선 / Gotchas 추가 / 스키마 변경)

### Step 6: Sprint Contract (DRAFT) + 개선안 작성

1. 현재 버전의 sprint-contract로 이번 카이젠의 Sprint Contract 작성
2. 개선안을 DRAFT로 작성 — **파일에 적용하지 않는다**
3. DRAFT를 대화에 출력하여 QA 대상으로 제시

### Step 7: QA + 적용 + Regression

1. 현재 버전의 qa-evaluator로 DRAFT 평가
2. APPROVE:
   - `kaizen-phase-2-pre` git tag 생성
   - 파일에 적용 + 커밋
   - Regression Smoke Test (`harness/evals/kaizen/contract-kaizen/` 활용)
   - Regression PASS → 완료
   - Regression FAIL → `git revert` + BLOCKED
3. REJECT:
   - 피드백 반영 → DRAFT 수정 → 재QA (최대 3회)
   - 3회 REJECT → 사용자 에스컬레이션

### Step 8: 기록

1. `docs/kaizen/research-log.md`에 엔트리 추가 (`templates/research-log-entry.md` 형식)
2. `docs/kaizen/changelog.md`에 변경 기록
3. 버전 bump 판단:
   - patch: docs, Gotchas 추가
   - minor: 스킬 프롬프트 변경, 스키마 변경
   - major: 아키텍처 변경

## 버전 bump 판단 가이드

| 변경 유형 | bump |
|-----------|------|
| contract-design-guide.md만 수정 | patch |
| Gotchas 추가/수정 | patch |
| Process 단계 변경 | minor |
| contract-schema.md 변경 | minor |
| sprint-contract 아키텍처 변경 | major |

## Step 9: Plugin Validation 결과 반영

카이젠 세션 시작/종료 시 `scripts/validate-plugin.py harness` 를 실행하여 7 카테고리 상태를 확인하고 결과를 개선 우선순위에 반영한다.

**실행 패턴, 우선순위 매핑, 통합 규칙**은 `harness/docs/guides/plugin-validation-guide.md §7` 에서 정의한다 (SSOT) — 해당 섹션을 그대로 따른다.

## References

- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 7 카테고리 기준 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
