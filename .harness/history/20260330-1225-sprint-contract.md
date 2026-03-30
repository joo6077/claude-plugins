---
feature: "kaizen-phase3: flutter-toolkit 업데이트 + flutter-test 초안"
created: "2026-03-30 20:00"
complexity: "중간"
conditions: 12
---

## Skill
- [ ] SK-01: flutter-audit에 `containsSemantics` → `isSemantics` 테스트 매처 변경 Gotcha가 추가된다
- [ ] SK-02: flutter-widget에 variable font weight 관련 Gotcha가 추가된다
- [ ] SK-03: flutter-test 초안 SKILL.md가 `flutter-toolkit/skills/flutter-test/`에 생성된다
- [ ] SK-04: flutter-test SKILL.md에 frontmatter(name, description, argument-hint, user-invocable)가 있다
- [ ] SK-05: flutter-test에 Gotchas 섹션이 존재한다 (최소 1개)
- [ ] SK-06: flutter-test에 기본 Process가 정의된다

## Architecture
- [ ] AR-01: flutter-test가 `flutter-toolkit/skills/flutter-test/SKILL.md` 경로에 존재한다

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
