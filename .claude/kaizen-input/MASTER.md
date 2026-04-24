# Kaizen Input — Master Index

생성일: 2026-04-24
목적: kaizen-orchestrator가 Phase별 개선 작업 시 읽을 **우선순위 데이터 묶음**. 각 Phase는 이 파일에서 자기 플러그인 섹션을 찾아 반영하라.

## 데이터 소스

1. **`/insights` 리포트** (`insights-report.md`) — 30일 세션 로그 패턴 (마찰점, 추천 패턴)
2. **Harness QA 피드백** (`plugin-qa-data.md`, `harness-feedback-summary.json`) — 138 evaluations + 34 contracts
3. **프로젝트별 피드백** (`per-project-feedback.md`) — 5개 프로젝트(.harness/)의 최근 sprint-contract/sprint-feedback
4. **Reflect-Kit reflections** (`reflect-aggregated.md`) — 1798 reflections 집계

## 핵심 수치 (Global stats)

| 지표 | 값 |
|------|---|
| 총 평가 수 | 138 |
| APPROVE | 77 |
| REJECT | 61 |
| **REJECT 비율** | **44%** — 개선 여지 큼 |
| 총 reflections | 1798 |
| tool_failure | 849 |
| misunderstanding | 419 |
| wrong_approach | 359 |
| repeated_error | 171 |

## 플러그인별 핵심 이슈 (요약)

### harness (approve=77, reject=61)
- 가장 많이 사용됨 (계약·평가가 메타 레이어라 모든 reject가 harness에도 잡힘)
- **SK-02**: Neubrutalism shadow offset 범위 모호성 → 계약 조건 명시 강화
- **H-01/H-03**: rust-init/rust-feature/rust-api Gotchas 원칙 누락 일관성 이슈
- **미검증 항목 경계**: mcp_server: null 상태에서 시각 검증 불가 → 조건 자동 분기
- **l3_unreached**: 13회 — L3 검증 샘플링으로 끝남

### design-kit (approve=0, reject=5)
- **SK-05**: design-concept/design-component 자동 로드가 Process Step이 아닌 별도 섹션에 있어 계약 불충족
- **PH-01**: agent-design-guide.md에 '계약 모호성 방지 원칙' 누락 (skill-design-guide.md §3.5 대응 없음)
- **I-02**: modified 파일 0건 조건의 예외 범위 명확화 필요
- **AR-01**: design-mockup 템플릿이 `.md` 패턴이 아닌 `.html` — 구조 일관성

### react-kit (approve=1, reject=4)
- **DG-01**: react-feature, react-widget 코드 템플릿 내 TODO 7건 — 계약 0건 조건 불충족
- **DG-02**: 5개 파일(react-init, react-run, react-build, react-preflight, react-audit, react-reviewer)에 언어 힌트 없는 fenced code block
- **AP-01**: react-form Gotchas에 Zustand/TanStack Query 상태 분리 원칙 미명시
- **RE-02**: 트리거 키워드 배타성 위반 (react-api "API 연동" ⊂ react-feature "API 연동 화면")

### infra-kit (approve=0, reject=4)
- **AR-03**: README.md 누락
- **AR-04**: evals/ 디렉토리 누락
- **SK-07/SK-08**: infra-audit, infra-init SKILL.md Step 3 비어있음
- **SK-13**: .claude/skills/infra-kaizen References 섹션 누락

### backend-kit (approve=0, reject=3)
- infra-kit와 동일 이슈 세트 (README, evals/, Step 3, References)
- **ER-01**: load_evals에서 JSONDecodeError 시 sys.exit(2) 추가 필요

### rust-kit (approve=0, reject=3)
- **H-01**: rust-init/rust-feature Gotchas에 domain event + outbox 원칙 누락
- **H-03**: rust-api Gotchas에 Composition Root 단일화 원칙 누락
- **SK-03**: rust-api 핸들러 예시에서 PgPool 직접 사용 (trait 추상화 없음)
- **AR-02**: 계획 파일 Goal 17개 vs 스펙 20개 리서치 문서 수 불일치

### flutter-toolkit (approve=0, reject=2)
- **I-01**: Fix commit push 미완료
- **I-02**: modified 파일 예외 목록 (sprint-feedback.md, README.md, history 아카이브) 명시 필요
- **create-kit Gotcha #2 위반**: 3종 스킬 패턴 대신 17종 워크플로우 패턴 선택 정당화
- **S2-02**: ops/ 리서치 문서 수 불일치 (ci-cd.md, observability.md 미처리)

### reflect-kit (approve=0, reject=2)
- **SC-05**: git tag reflect-kit/v0.2.0 로컬 미생성
- **AP-01**: README.md 버전 하드코딩 (plugin.json v0.2.0과 불일치)
- **ER-01**: log-reflection.sh에 redact_sensitive() 호출 누락 — 보안 위험
- **SK-06**: reflect-digest/SKILL.md에 Gotchas/Process 섹션 미존재
- **AP-03**: reflect-kit/docs/DESIGN.md bare code fence

## /insights에서 나온 워크플로우 이슈 (전체 Phase 공통 반영)

1. **Proactive quality gaps**: 리팩토링 시 규칙에 있는 개선점을 놓침 → 편집 전 전체 규칙 위반 리스트업
2. **Wrong approach & false dichotomies**: 토큰/코드 검증 없이 약속 → Figma/코드/계약 enumerate-before-act
3. **Session truncation**: 출력 토큰 제한, sandbox 차단, 백그라운드 에이전트 멈춤 → 청크 단위 커밋, SESSION_LOG 유지

## Phase별 주입 규칙

각 Phase는 자기 플러그인 섹션을 반드시 읽고:

1. **REJECT reasons에 적힌 구체적 FAIL 항목**을 Sprint Contract 조건으로 편입
2. **improvement_suggestions**를 Process/Gotchas에 녹여넣기
3. **/insights 3대 마찰점**은 모든 Phase 공통 체크리스트로 적용

Phase 0 (설계 가이드)는 harness 공통 이슈(`l3_unreached`, `contract_misinterpret`, `perspective_gap`)를 특히 주목.
