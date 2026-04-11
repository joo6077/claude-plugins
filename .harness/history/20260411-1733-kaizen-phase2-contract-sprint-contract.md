---
feature: "Phase 2 Contract 카이젠 — contract-design-guide 구체성 레벨 + 예외 조항 패턴 추가"
created: "2026-04-10 18:00"
complexity: "단순"
conditions: 8
---

## Docs

- [ ] DC-01: `contract-design-guide.md`에 "조건 구체성 레벨" 섹션이 추가된다. exact/structural/goal 3단계 정의와 각 단계별 사용 기준이 명시된다.
- [ ] DC-02: `contract-design-guide.md`에 "예외 조항 포맷" 패턴이 추가된다. `조건ID: ... 예외: (a) ..., (b) ...` 형태의 인라인 예외 명시 가이드가 포함된다.
- [ ] DC-03: `contract-design-guide.md`에 "검증 대상 파일 범위 한정" 가이드가 추가된다. 파일 타입/성격에 따라 조건 적용 범위를 제한하는 `applies_to` 개념이 설명된다.
- [ ] DC-04: `contract-design-guide.md`의 안티패턴 테이블에 "판정 기준 범주 미명시" 항목이 추가된다. exact(이름 일치) vs goal(목표 달성) 중 어느 기준으로 판정할지 계약에 명시하지 않은 경우를 나쁜 예로 수록한다.

## Skills

- [ ] SK-01: `sprint-contract/SKILL.md` Gotchas에 "조건 작성 시 판정 기준 범주(exact/structural/goal)를 명시하라"는 항목이 추가된다.
- [ ] SK-02: `sprint-contract/SKILL.md` Gotchas에 "예외 케이스는 조건 내부에 인라인으로 명시하라"는 항목이 추가된다. 별도 문서 분리나 구두 합의가 아닌 계약 텍스트 내 명시를 요구한다.

## Anti-patterns

- [ ] AP-01: 기존 문서 섹션을 전면 재작성하지 않는다. 섹션 추가 또는 기존 예시 보강만 허용한다.
- [ ] AP-02: 데이터 풀 §1에서 실제로 발생한 케이스만 인용한다. 창작된 예시를 가이드에 포함하지 않는다.

## Reusability

- [ ] RE-01: 추가된 개념(구체성 레벨, 예외 조항)이 harness 외 다른 플러그인 계약 작성에도 범용 적용 가능한 형태로 기술된다.
- [ ] RE-02: 기존 가이드 구조(핵심 원칙 → 조건 작성법 → 카테고리 설계 → 안티패턴 → 자기개선)와 일관된 섹션 위계를 유지한다.

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py` 실행 시 Phase 2 변경 파일(`contract-design-guide.md`, `sprint-contract/SKILL.md`)로 인한 신규 harness 오류가 없다. 예외: Phase 2 이전부터 존재한 기존 오류(V5 placeholder, V6 bare fence)는 적용 제외 [L3]
- [ ] DG-02: 수정된 SKILL.md frontmatter YAML 파싱 오류 0건
- [ ] DG-03: `python3 scripts/sync-docs.py --check-only` 실행 시 동기화 필요 알림이 없거나 변경 내용과 무관한 항목만 알림
