---
feature: "react-kit Phase 5: G4 Quality Skills (3종)"
created: "2026-04-10T20:20:00+09:00"
complexity: "복잡"
conditions: 15
scope: "react-kit/skills/ 에 3개 G4 스킬 (/react-test, /react-error, /react-l10n) SKILL.md 추가. 소스: docs/react/kit-design/g4-quality.md"
---

## Skill
- [ ] SK-01: `react-kit/skills/react-test/SKILL.md` 존재. frontmatter 유효 + name=react-test
- [ ] SK-02: `react-kit/skills/react-error/SKILL.md` 존재. frontmatter 유효 + name=react-error
- [ ] SK-03: `react-kit/skills/react-l10n/SKILL.md` 존재. frontmatter 유효 + name=react-l10n
- [ ] SK-04: 각 스킬 description 에 한국어/영어 트리거 키워드 3개 이상
- [ ] SK-05: 각 스킬의 Gotchas 섹션이 g4-quality.md 의 §1.8 / §2.8 / §3.7 Gotchas 반영
- [ ] SK-06: 각 스킬의 Process 섹션이 g4-quality.md 의 §X.3~§X.6 (Clean Arch 레이어별 전략, 패턴, 흐름) 반영

## Script
- [ ] SC-01: 모든 SKILL.md frontmatter YAML parse 가능
- [ ] SC-02: `python3 scripts/sync-docs.py --check-only react-kit` 실행 시 AUTO:skills 블록이 Phase 2+3+4+5 합계 13개 스킬 포함

## Architecture
- [ ] AR-01: `/react-test` 가 Clean Architecture 레이어별 테스트 전략 (domain=unit, data=integration with MSW, presentation=component with RTL, e2e=Playwright) 을 명시
- [ ] AR-02: `/react-error` 가 3단계 에러 처리 흐름 (데이터 경계 → Failure 전파 → UI 표시) 을 명시하고 `references/result-patterns.md` 참조

## Anti-patterns
- [ ] AP-01: `/react-test` 에 "Clean Arch 레이어 위반 테스트 금지" (예: domain 레이어 테스트가 data 모킹 없이 직접 fetch 호출) 규칙 명시
- [ ] AP-02: `/react-error` 에 "Error Boundary 는 presentation 레이어 루트에서만" 규칙 명시 (`React.ErrorBoundary`) + Severity 매핑 규칙
- [ ] AP-03: `/react-l10n` 에 "번역 키 하드코딩 금지, 모든 문자열은 `t`/`<Trans>` 매크로 경유" 규칙 명시

## Reusability
- [ ] RE-01: SKILL.md 구조 기존 스킬과 일관
- [ ] RE-02: Phase 2+3+4+5 총 13개 스킬 트리거 키워드 상호 배타적

## Diagnostics
- [ ] DG-01: SKILL.md 파일 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-02: 모든 fenced code block 에 언어 힌트
