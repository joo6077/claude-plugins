---
feature: "create-skill, create-agent 스킬 생성"
created: "2026-03-30 19:00"
complexity: "중간"
conditions: 18
---

## Skill
- [ ] SK-01: create-skill SKILL.md에 YAML frontmatter(name, description, argument-hint, user-invocable)가 있다
- [ ] SK-02: create-agent SKILL.md에 YAML frontmatter(name, description, argument-hint, user-invocable)가 있다
- [ ] SK-03: create-skill description에 트리거 키워드("스킬 만들어줘", "create skill")와 비트리거 조건(기존 스킬 수정 제외)이 포함된다
- [ ] SK-04: create-agent description에 트리거 키워드("에이전트 만들어줘", "create agent")와 비트리거 조건(스킬로 충분한 경우 제외)이 포함된다
- [ ] SK-05: 두 스킬 모두 Gotchas 섹션이 존재하고 최소 3개 항목이 있다
- [ ] SK-06: create-skill의 Process가 설계 가이드(docs/guides/skill-design-guide.md)를 읽는 단계로 시작한다
- [ ] SK-07: create-agent의 Process가 설계 가이드(docs/guides/agent-design-guide.md)를 읽는 단계로 시작한다
- [ ] SK-08: create-agent에 "스킬로 충분한지 먼저 판단" 단계가 포함된다

## Architecture
- [ ] AR-01: create-skill이 `harness/skills/create-skill/SKILL.md` 경로에 존재한다
- [ ] AR-02: create-agent가 `harness/skills/create-agent/SKILL.md` 경로에 존재한다
- [ ] AR-03: 두 스킬 모두 설계 가이드를 자체 포함하지 않고 `docs/` 경로를 참조한다

## Error
- [ ] ER-01: create-skill에 검증 체크리스트(frontmatter, description, Gotchas 확인)가 포함된다
- [ ] ER-02: create-agent에 검증 체크리스트(필수 필드, 도구 제한, 모델 선택 확인)가 포함된다

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다
- [ ] AP-02: force push 금지

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
