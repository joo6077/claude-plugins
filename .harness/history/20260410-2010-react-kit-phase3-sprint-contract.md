---
feature: "react-kit Phase 3: G2 State & Data Skills (4종)"
created: "2026-04-10T19:55:00+09:00"
complexity: "복잡"
conditions: 16
scope: "react-kit/skills/ 에 4개 G2 스킬 (/react-store, /react-api, /react-query, /react-form) SKILL.md 추가. 소스: docs/react/kit-design/g2-state-data.md"
---

## Skill
- [ ] SK-01: `react-kit/skills/react-store/SKILL.md` 존재. frontmatter 에 name=react-store, description (트리거 키워드 포함), user-invocable=true, argument-hint 명시
- [ ] SK-02: `react-kit/skills/react-api/SKILL.md` 존재. frontmatter 유효 + name=react-api
- [ ] SK-03: `react-kit/skills/react-query/SKILL.md` 존재. frontmatter 유효 + name=react-query
- [ ] SK-04: `react-kit/skills/react-form/SKILL.md` 존재. frontmatter 유효 + name=react-form
- [ ] SK-05: 각 스킬 description 에 한국어/영어 트리거 키워드 3개 이상 포함
- [ ] SK-06: 각 스킬의 Gotchas 섹션이 g2-state-data.md 의 해당 §X.6 (또는 §X.4.6, §X.7 등 Gotchas 서브섹션) 내용을 반영
- [ ] SK-07: 각 스킬의 Process 섹션이 g2-state-data.md 의 해당 §X.3~§X.5 (파일 구조, 패턴, 세부 흐름) 를 반영

## Script
- [ ] SC-01: 모든 SKILL.md 의 frontmatter YAML 이 parse 가능하다
- [ ] SC-02: `python3 scripts/sync-docs.py --check-only react-kit` 실행 시 README 의 AUTO:skills 블록이 Phase 2+3 합계 8개 스킬을 포함한다

## Architecture
- [ ] AR-01: 4개 스킬 모두 `references/clean-arch-layout.md` 의 레이어 규칙을 따른 경로 생성 (react-store=presentation/shared/stores, react-api=4레이어 연쇄, react-query=presentation/features/hooks, react-form=presentation/features/hooks)
- [ ] AR-02: `/react-api` 스킬은 `references/result-patterns.md` 의 neverthrow Result 패턴을 반드시 적용 (domain/data 레이어에서 throw 금지, Result<T, Failure> 시그니처)

## Anti-patterns
- [ ] AP-01: 4개 스킬 모두 상태 분리 원칙 (Zustand=클라이언트 상태, TanStack Query=서버 상태) 를 명시하거나 위반을 방지하는 Gotchas 포함
- [ ] AP-02: `/react-api` 의 domain 레이어에서 `throw` 금지 규칙 명시 (Result 반환만 허용)
- [ ] AP-03: `/react-query` 에서 queryKey 네이밍 규칙 (`g2-state-data.md §3.3`) 명시

## Reusability
- [ ] RE-01: SKILL.md 구조가 기존 rust-kit/flutter-toolkit 스킬과 일관 (frontmatter → Gotchas → Process)
- [ ] RE-02: Phase 2 에서 추가한 G1 4개 스킬 + Phase 3 G2 4개 스킬 총 8개의 트리거 키워드가 상호 배타적 (예: "기능" 은 /react-feature, "API 연동" 은 /react-api)

## Diagnostics
- [ ] DG-01: 4개 SKILL.md 파일 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-02: 4개 SKILL.md 파일의 마크다운 코드 블록이 닫혀있고 언어 힌트 명시됨 (빈 ` ``` ` 금지)
