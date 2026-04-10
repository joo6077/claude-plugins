---
feature: "react-kit Phase 2: G1 Scaffolding Skills (4종)"
created: "2026-04-10T19:45:00+09:00"
complexity: "복잡"
conditions: 16
scope: "react-kit/skills/ 에 4개 G1 스킬 (/react-init, /react-screen, /react-feature, /react-widget) SKILL.md 추가. 소스: docs/react/kit-design/g1-scaffolding.md (525 lines)"
---

## Skill
- [ ] SK-01: `react-kit/skills/react-init/SKILL.md` 존재. frontmatter 에 name=react-init, description (트리거 키워드 포함), user-invocable=true, argument-hint 명시
- [ ] SK-02: `react-kit/skills/react-screen/SKILL.md` 존재. frontmatter 유효 + name=react-screen
- [ ] SK-03: `react-kit/skills/react-feature/SKILL.md` 존재. frontmatter 유효 + name=react-feature
- [ ] SK-04: `react-kit/skills/react-widget/SKILL.md` 존재. frontmatter 유효 + name=react-widget
- [ ] SK-05: 각 스킬 description 에 트리거 키워드 3개 이상 (한국어/영어 혼합) 포함
- [ ] SK-06: 각 스킬의 Gotchas 섹션이 존재하며 g1-scaffolding.md 의 해당 §X.6 Gotchas 내용을 반영
- [ ] SK-07: 각 스킬의 Process 섹션이 존재하며 g1-scaffolding.md 의 §X.3 (산출물/파일 트리) 과 §X.4 (생성 명령 순서) 를 반영

## Script
- [ ] SC-01: 모든 SKILL.md 의 frontmatter YAML 이 parse 가능하다 (`python3 -c "import yaml; ..."` 통과)
- [ ] SC-02: `python3 scripts/sync-docs.py --check-only react-kit` 실행 시 README 의 AUTO:skills 블록이 4개 스킬을 포함하도록 동기화된다

## Architecture
- [ ] AR-01: 모든 4개 스킬이 `references/project-detection.md` 를 참조 (문서 내 명시적 링크 또는 파일명 언급)
- [ ] AR-02: 모든 4개 스킬이 생성하는 경로가 `references/clean-arch-layout.md` 의 레이어 규칙 (domain/, data/, presentation/, infrastructure/) 을 따른다

## Anti-patterns
- [ ] AP-01: 모든 4개 스킬에 "중복 감지 필수 (overwrite 금지, --force 플래그 명시)" 규칙이 Gotchas 또는 Process 에 포함
- [ ] AP-02: 모든 4개 스킬에 "Strict TypeScript 강제" 규칙 (`tsc --noEmit`, `eslint --max-warnings=0`, `any`/`as`/`!` 금지) 이 명시
- [ ] AP-03: design doc 의 공통 설계 원칙 "실패 시 롤백" 규칙이 각 스킬에 명시

## Reusability
- [ ] RE-01: SKILL.md 구조가 기존 `rust-kit/skills/*/SKILL.md` 또는 `flutter-toolkit/skills/*/SKILL.md` 와 일관된다 (frontmatter → Gotchas → Process 순서)
- [ ] RE-02: 4개 스킬의 트리거 키워드가 명확히 구분되어 겹침이 없다 (/react-init 은 새 프로젝트, /react-screen 은 라우트/화면, /react-feature 는 4계층 복합 생성, /react-widget 은 재사용 컴포넌트)

## Diagnostics
- [ ] DG-01: 4개 SKILL.md 파일 내 placeholder (TODO, TBD, FIXME, "나중에") 0건
- [ ] DG-02: 4개 SKILL.md 파일의 마크다운 코드 블록이 닫혀있고 언어 힌트가 명시됨
