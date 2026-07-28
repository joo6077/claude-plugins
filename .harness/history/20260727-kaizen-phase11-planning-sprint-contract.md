# Sprint Contract — Phase 11 (planning-kit) kaizen 2026-07-27

- Branch: `kaizen/2026-07-27`
- Scope: `planning-kit/agents/planning-reviewer.md`, `planning-kit/skills/plan-audit/SKILL.md`,
  `planning-kit/skills/plan-stories/SKILL.md`, `.claude/skills/planning-kaizen/SKILL.md`,
  `docs/planning/research-log.md`
- 신호 농도: LOW (외부 프로젝트 planning-kit 사용 0건, reflect-digest planning 결함 0건).
  research-only 모드. 억지 변경 금지 — 실측 불일치와 Phase 1/3/4 정합화만 처리한다.

## 리서치 (WebFetch 6건 — Context7 미인증이라 미사용)

| # | URL | 확인 사실 |
|---|-----|----------|
| 1 | https://cucumber.io/docs/gherkin/reference | "An outcome _should_ be on an **observable** output ... not a behaviour deeply buried inside the system" · "we recommend 3-5 steps per example" · Then 은 actual vs expected 비교 |
| 2 | https://agilealliance.org/glossary/invest/ | Testable = "in principle, even if there isn't a test for it yet" (원리적 반증가능성이 기준) |
| 3 | https://basecamp.com/shapeup/1.5-chapter-06 | "the first step for presenting a pitch is posting the write-up ... somewhere that stakeholders can read it on their own time" → pitch 는 구두 아이디어가 아닌 **기록 아티팩트** |
| 4 | https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects | sub-issue · issue dependencies(blocked by/blocking) · "Have a single source of truth" · Projects 자동화는 **GraphQL API** 만 언급 |
| 5 | https://www.svpg.com/four-big-risks/ | 4 risks 정의 유지 · "Tackle the big risks *early*" |
| 6 | https://www.producttalk.org/glossary-discovery-opportunity-solution-tree/ | OST 4 노드 (Desired Outcome / Opportunity / Solution / Assumption Tests) · "makes implicit assumptions explicit" |

리서치 결론: 외부 방법론 쪽 drift 없음. plan-sync-github Gotcha 4(Projects v2=GraphQL) ·
Gotcha 10(sub-issue+dependency) · plan-audit cat 6(3-5 step, 관찰 가능) 모두 현행 출처와 일치.
→ 외부 리서치 기인 변경 0건. 아래 조건은 전부 **내부 정합화**다.

## Conditions

| ID | 조건 | 판정 기준 | 근거 |
|----|------|----------|------|
| P11-01 | `planning-reviewer.md` 에 Canonical Unverified-Evidence Protocol 5 조항을 **문구 변형 없이** 복제하고 SSOT 앵커를 명시 | 5 조항 텍스트가 `qa-evaluation-guide.md` L431-446 과 문자열 동일 (백틱 포함). 앵커 문구 `§Canonical Unverified-Evidence Protocol` 존재 | Phase 3 v4.0 지목 drift |
| P11-02 | planning-reviewer 의 "[미검증] 도 0" 요구 제거 → 임계 2 로 통일 | Step 4 에 0/1/2+ 3분기 존재. `[미검증] 도 0` 문자열 부재. 자기 문서에서 임계값 재정의 없음 (canonical 인용만) | canonical 조항 3 |
| P11-03 | `N/A` 오독 방지 주석 — 본 킷 `N/A` 는 선택 카테고리 비적용이며 `[미검증]` 동의어가 아님 | verbatim 블록 **밖**에 주석 1줄. verbatim 블록 자체는 무변형 | canonical 조항 1 이 N/A 를 금지 동의어로 열거 → 내부 모순 방지 |
| P11-04 | Evidence Validity Gate 3분기 반영 — 파일은 있으나 섹션이 공허하면 PASS 아님 | planning-reviewer Step 2 에 "존재하지만 공허" 분기 1줄 (조항 2 인용) | skill-design-guide §3.7 조항 4 · canonical 조항 2 |
| P11-05 | `plan-audit` Step 5 verdict 규칙을 P11-02 와 Sibling Consistent 하게 갱신 + 미검증 집계 의무 | Step 5 에 미검증 0/1/2+ 분기. Summary 템플릿에 건별 `[항목 ID, 사유, fallback]` | canonical 조항 3·5 · Sibling Consistency |
| P11-06 | `plan-stories` AC 의 falsifiability 강화 — INVEST T 행에 "AC 가 거짓임을 보여줄 관측" 요구 | Step 4 T 행에 반증 관측 요구 문구 + INVEST 출처 인용 | INVEST "Testable in principle" · Cucumber actual vs expected |
| P11-07 | `plan-stories` 에 two-sided(양면) AC 요구 — 계약 경계를 넘는 스토리는 producer/consumer 면을 열거하고 산출물에 남긴다 (E2) | Gotcha 1건 + Step 6 저장 템플릿에 양면 열거 섹션 | skill-design-guide §5.5 Counterpart Enumeration (parity 12, 생성 측 전용) · §0 Friction #4 |
| P11-08 | evaluator 측 Counterpart 대응 절을 **만들지 않는다** (의도된 부재) | `plan-audit` / `planning-reviewer` 에 counterpart/양면 카테고리 신규 추가 0건 | parity item 12 "평가자는 계약 조건으로 수용" |
| P11-09 | `planning-kaizen/SKILL.md` 의 validate-plugin "7 카테고리" → "8 카테고리 (V1~V8)" | `7 카테고리` 문자열 부재, `V1~V8` 존재 | Phase 4 |
| P11-10 | `docs/planning/research-log.md` 에 2026-07-27 엔트리 (URL 5건 이상) | 엔트리 존재 + URL 6건 | 오케스트레이터 제약 |
| P11-11 | 신규 규칙 남발 금지 — 직전 사이클 승격분(8스킬 scope-discipline) 재추가 0건 | `git diff` 에 scope-discipline 문구 신규 추가 없음 | insights-report "이미 승격 완료 — 중복 금지" |
| P11-12 | 회귀 없음 | `python3 scripts/validate-plugin.py planning-kit` → V1~V8 all OK | — |

## 명시적 비범위 (검토 후 기각)

- **스테일 핸드오프 git 재검증** (§0 Friction #5): insights-report 가 **Phase 4 Harness** 로 배정.
  planning-kit 에 중복 승격하지 않는다.
- **plan-prd**: Shape Up 아티팩트 요구(출처 3)와 기준선 있는 success metric(Step 4 체크리스트)로
  이미 falsifiable + committed-artifact 충족. 변경 없음.
- **plan-sync-github**: 출처 4 와 현행 Gotcha 일치. 변경 없음.
- **plan-data-model PlantUML 옵션 / Projects REST→GraphQL 마이그레이션 가이드**: 이전 사이클 백로그이나
  이번 신호 농도 LOW + 사용 흔적 0 → 착수 근거 없음. 백로그 유지.
- 나머지 8 스킬(ideate/reference/discover/prioritize/flow/data-model/risks/guide): 갭 미발견, 무변경.
