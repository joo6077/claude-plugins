---
feature: "design-component SKILL.md 리서치 기반 개선"
created: "2026-04-09 16:00"
complexity: "낮음"
conditions: 9
---

## Skill
- [x] SK-01: Given SKILL.md의 Gotchas 섹션을 확인할 때, Then 커스터마이징 옵션 누락 금지(5), API Doc 헤더 필수(6), Anatomy 누락 금지(7), 접근성 섹션 누락 금지(8), When to use 누락 금지(9) 총 5개 신규 Gotcha가 존재한다
- [x] SK-02: Given SKILL.md의 Step 2-1을 확인할 때, Then 산출물 섹션 구조가 12개 항목(Purpose→When to use→Anatomy→Preview→Variants→States→Sizes→Props→Accessibility→Tokens→Do/Dont→Related) 순서로 정의되어 있다
- [x] SK-03: Given SKILL.md의 Step 2-2를 확인할 때, Then API Doc 헤더 예시에 Props 테이블이 Prop/Type/Allowed Values/Default/Required/Description 6개 필드를 포함한다
- [x] SK-04: Given SKILL.md의 Step 2-2를 확인할 때, Then API Doc 헤더 예시에 When to use/When not to use 섹션이 포함되어 있다
- [x] SK-05: Given SKILL.md의 Step 2-2를 확인할 때, Then API Doc 헤더 예시에 Anatomy 섹션이 포함되어 있고 필수/선택 part가 구분되어 있다
- [x] SK-06: Given SKILL.md의 Step 2-2를 확인할 때, Then API Doc 헤더 예시에 Accessibility 섹션이 ARIA 역할, 키보드 인터랙션, 라벨링 요구사항을 포함한다
- [x] SK-07: Given SKILL.md의 Step 2-3 커스터마이징 옵션 체크리스트를 확인할 때, Then 기존 10개 + 신규 5개(icon, orientation, placement, density, controlled) 총 15개 옵션이 정의되어 있다

## Architecture
- [x] AR-01: SKILL.md가 design-kit/skills/design-component/SKILL.md에 존재하며 frontmatter(name, description, argument-hint, user-invocable)가 유효하다

## Anti-patterns
- [x] AP-01: 구현 코드(Flutter/React/CSS)가 SKILL.md에 포함되지 않았다 — 디자인 스펙 예시만 포함
