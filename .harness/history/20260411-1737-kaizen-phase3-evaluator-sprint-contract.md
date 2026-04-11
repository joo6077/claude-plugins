# Sprint Contract

Feature: Phase 3 Kaizen — qa-evaluation-guide + qa-evaluator 개선
Date: 2026-04-10
Complexity: 중간 (2 파일 수정, 구조 추가)
Sprint: kaizen-phase3-evaluator

---

## 완료 조건

### TC (Term Clarity) — 용어 충돌 해결

- [ ] TC-01: `qa-evaluation-guide.md`에 "용어 구분" 섹션이 존재하고, `[L1/L2/L3]`이 evaluator 검증 깊이(존재/내용/의미)를 의미하며, 계약의 구체성 레벨(exact/structural/goal)과 다른 개념임을 명시한다 [L2]
- [ ] TC-02: `qa-evaluation-guide.md` 용어 구분 섹션에 두 체계를 혼동 방지하는 빠른 참조 표(검증 깊이 vs 구체성 레벨)가 존재한다 [L2]
- [ ] TC-03: `qa-evaluator.md`의 검증 깊이(L1/L2/L3) 테이블 또는 근처에 "계약의 [Lx] 태그(exact/structural/goal)와 동일 기호지만 의미 다름" 주의 문구가 존재한다 [L2]

### SE (Set Intersection) — 키워드 배타성 검증

- [ ] SE-01: `qa-evaluation-guide.md`에 스킬 트리거 키워드 배타성 검증 절차 섹션이 존재한다 [L2]
- [ ] SE-02: 해당 섹션에 "Grep으로 키워드를 추출 → 다른 스킬 SKILL.md 목록과 교차 비교(set intersection)" 절차가 명시된다 [L3]
- [ ] SE-03: 부분 문자열 포함 관계(예: "API 연동" vs "API 연동 화면")도 배타성 위반으로 판정해야 한다는 규칙이 명시된다 [L2]

### L3C (L3 Coverage) — 심층 검증 강화

- [ ] L3C-01: `qa-evaluation-guide.md`의 L3 검증 절차에 "관련 파일 전체 Read 후 의미 매칭" 지침이 추가된다 [L2]
- [ ] L3C-02: 해당 지침에 "Grep으로 존재 확인 후 Read로 전체 내용 확인 → 의도된 의미로 동작하는지 추적"의 2단계 흐름이 명시된다 [L3]

### DG (DG-02 Alternative) — HTML 코드블록 대체 절차

- [ ] DG-01: `qa-evaluation-guide.md`에 HTML 기반 프로젝트에서의 DG-02(코드블록 언어 힌트) 검증 시 대체 패턴(예: HTML 파일의 `<code>` 태그 또는 `<pre>` 블록 언어 명시) 또는 적용 제외 기준이 언급된다 [L2]

### ST (Structure) — 기존 구조 유지

- [ ] ST-01: `qa-evaluation-guide.md`의 기존 섹션 제목과 순서가 유지된다 [L1]
- [ ] ST-02: `qa-evaluator.md`의 기존 섹션(Process Step 1~9, 판정 규칙, Red Flags, Rationalization Table, References) 구조가 유지된다 [L1]

---

## 안티패턴

- `qa-evaluation-guide.md`에서 기존 검증 방법론 섹션(3-Level 검증, Rubric 기반 분해 등)을 삭제하거나 대폭 재작성하지 않는다
- Phase 2 결과(`contract-design-guide.md`의 구체성 레벨 체계)를 수정하지 않는다
- 용어 구분 설명을 qa-evaluator.md의 핵심 판정 흐름 중간에 삽입하여 가독성을 해치지 않는다
