---
feature: "/release 커맨드 스킬"
created: "2026-03-29 20:30"
complexity: "단순"
conditions: 10
---

## Skill
- [ ] SK-01: `.claude/commands/release.md` 파일이 존재한다
- [ ] SK-02: frontmatter에 `description` 필드가 있고 릴리스/버전 bump 관련 설명이 포함되어 있다
- [ ] SK-03: frontmatter에 `argument-hint`가 `<plugin-name> <patch|minor|major>` 형식으로 있다
- [ ] SK-04: 스킬 본문에 `$ARGUMENTS` 파싱 규칙이 명시되어 있다

## Script
- [ ] SC-01: 스킬이 `bash scripts/release.sh` 명령을 호출하도록 안내한다
- [ ] SC-02: release.sh가 plugin.json의 version 필드를 업데이트한다
- [ ] SC-03: release.sh가 marketplace.json의 description 내 `[vX.Y.Z · YYYY-MM-DD]` 패턴을 업데이트한다

## Error
- [ ] ER-01: 인자가 부족할 때 사용자에게 플러그인 목록과 bump 타입을 안내한다
- [ ] ER-02: dirty working tree 경고 시 사용자 확인을 받도록 안내한다

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다
- [ ] AP-02: force push를 사용하지 않는다

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 테스트 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 구동 시 에러 0개
