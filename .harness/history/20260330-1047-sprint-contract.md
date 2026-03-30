---
feature: "flutter-toolkit 모노레포 마이그레이션 + skill-design-guide 적용"
created: "2026-03-29 18:00"
complexity: "복잡"
conditions: 15
---

## Skill
- [ ] SK-01: 독립 위치의 15개 스킬 폴더가 모두 claude-plugins/flutter-toolkit/skills/에 존재한다
- [ ] SK-02: evals/evals.json이 claude-plugins/flutter-toolkit/evals/에 존재한다
- [ ] SK-03: references/project-detection.md가 claude-plugins/flutter-toolkit/references/에 존재한다
- [ ] SK-04: flutter-toolkit/plugin.json의 author, repository, license가 모노레포 표준(harness/plugin.json)과 동일한 형식이다
- [ ] SK-05: 15개 스킬의 description이 트리거 조건 형식이다 — "~할 때 사용" 또는 비트리거 조건을 포함한다
- [ ] SK-06: fit-pal 실전 경험 기반 Gotchas가 관련 스킬에 추가되어 있다 (최소 10개 스킬에 1개 이상)

## Error
- [ ] ER-01: flutter-toolkit/README.md에서 "(마이그레이션 예정)" 문구가 제거되고 실제 스킬 15개 목록으로 업데이트되어 있다

## Architecture
- [ ] AR-01: 마이그레이션된 스킬의 핵심 로직이 원본과 동일하다 — description/Gotchas 외에 본문 변경 없음
- [ ] AR-02: flutter-toolkit/ 폴더 구조가 모노레포 표준 패턴이다 (.claude-plugin/, skills/, evals/, references/)
- [ ] AR-03: .claude-plugin/marketplace.json에 flutter-toolkit 항목이 등록되어 있다
- [ ] AR-04: Gotchas 내용이 fit-pal의 실제 근거(CLAUDE.md, project.yaml anti_patterns, sprint-feedback)에 기반한다

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다
- [ ] AP-02: force push를 사용하지 않는다

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
