---
feature: "스킬 개선 + QA Evaluator 기본 엄격도 강화"
created: "2026-03-29 17:00"
complexity: "중간"
conditions: 14
---

## Skill
- [ ] SK-01: init/SKILL.md에 Gotchas 섹션이 존재하고, Claude가 반복 실패할 수 있는 지점이 1개 이상 기록되어 있다
- [ ] SK-02: sprint-contract/SKILL.md에 Gotchas 섹션이 존재하고, Claude가 반복 실패할 수 있는 지점이 1개 이상 기록되어 있다
- [ ] SK-03: sprint-contract의 긴 본문(Red Flags, Rationalization Table)이 별도 references/ 파일로 분리되어 있다
- [ ] SK-04: sprint-contract/SKILL.md 본문에 폴더 내 파일 목록이 명시되어 있어 Claude가 필요할 때 읽을 수 있다
- [ ] SK-05: qa-evaluator.md의 Red Flags 섹션에서 "관대함은 버그다"가 기본 동작으로 강화되어 있다 — 기존 "넘기면 프로덕션에서 터진다"보다 구체적인 차단 규칙 추가

## Architecture
- [ ] AR-01: 분리된 파일의 경로가 스킬 폴더 기준 상대 경로로 참조된다
- [ ] AR-02: SKILL.md의 기존 프로세스(6단계)와 핵심 규칙이 변경되지 않는다
- [ ] AR-03: init 스킬은 단순 스킬(62줄)이므로 폴더 확장 없이 Gotchas만 추가한다

## Error
- [ ] ER-01: 분리된 references 파일이 존재하지 않을 때 SKILL.md 본문만으로도 스킬이 동작 가능하다

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다
- [ ] AP-02: force push를 사용하지 않는다

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
