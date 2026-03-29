---
feature: "harness init 스킬"
created: "2026-03-29 21:00"
complexity: "단순"
conditions: 14
---

## Skill
- [ ] SK-01: `harness/skills/init/SKILL.md` 파일이 존재한다
- [ ] SK-02: frontmatter에 `name: init`이 있다
- [ ] SK-03: frontmatter에 `user-invocable: true`가 있다
- [ ] SK-04: frontmatter에 `argument-hint`가 있고 stack 인자를 안내한다
- [ ] SK-05: 본문에 `.harness/` 존재 여부를 먼저 확인하도록 명시되어 있다
- [ ] SK-06: 본문에 스택 자동 감지 로직이 명시되어 있다 (pubspec.yaml, Cargo.toml, package.json 등)
- [ ] SK-07: 본문에 `scripts/init.sh` 실행 방법이 명시되어 있다

## Script
- [ ] SC-01: `harness/scripts/init.sh` 파일이 존재한다
- [ ] SC-02: init.sh가 `.harness/project.yaml`을 생성한다
- [ ] SC-03: init.sh가 `.harness/procedures/` 디렉토리와 카테고리별 파일을 생성한다
- [ ] SC-04: init.sh가 인자로 받은 stack 값을 project.yaml에 반영한다

## Error
- [ ] ER-01: init.sh가 `.harness/`가 이미 존재하면 에러 메시지를 출력하고 종료한다
- [ ] ER-02: init.sh가 대상 디렉토리가 존재하지 않으면 에러 메시지를 출력하고 종료한다

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다
- [ ] AP-02: force push를 사용하지 않는다
