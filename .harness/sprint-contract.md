---
feature: "나머지 3개 스킬 리서치 기반 개선 (system/guide/audit)"
created: "2026-04-09 19:30"
complexity: "중간"
conditions: 9
---

## Skill
- [ ] SK-01: Given design-system SKILL.md를 확인할 때, Then Gotchas가 7개 이상이고 "3계층 토큰 아키텍처(primitive→semantic→component)" 관련 Gotcha가 존재한다
- [ ] SK-02: Given design-system SKILL.md를 확인할 때, Then "다크모드 토큰 네이밍" 관련 Gotcha가 존재한다 (color-dark-* 안티패턴)
- [ ] SK-03: Given design-guide SKILL.md를 확인할 때, Then Gotchas가 7개 이상이고 "우선순위 없는 나열 금지" 관련 Gotcha가 존재한다
- [ ] SK-04: Given design-guide SKILL.md를 확인할 때, Then 산출물 포맷에 "문제/원칙/제안/근거" 구조가 정의되어 있다
- [ ] SK-05: Given design-audit SKILL.md를 확인할 때, Then Gotchas가 7개 이상이고 "심각도 분류 필수(Critical/Major/Minor)" 관련 Gotcha가 존재한다
- [ ] SK-06: Given design-audit SKILL.md를 확인할 때, Then "주관적 판정 금지" 관련 Gotcha가 존재한다

## Architecture
- [ ] AR-01: 3개 SKILL.md 모두 frontmatter가 유효하다
- [ ] AR-02: design-audit의 audit-report.md 템플릿에 심각도별 섹션이 분리되어 있다

## Anti-patterns
- [ ] AP-01: 3개 SKILL.md에 구현 코드가 포함되지 않았다
