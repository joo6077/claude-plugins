---
feature: "flutter-kaizen 스킬 생성"
created: "2026-03-30 15:00"
complexity: "중간"
conditions: 18
---

## Skill
- [ ] SK-01: `SKILL.md`에 YAML frontmatter(name, description, argument-hint, user-invocable)가 있다
- [ ] SK-02: description에 트리거 키워드("/flutter-kaizen", "플러터 카이젠", "flutter 개선")가 포함된다
- [ ] SK-03: Gotchas 섹션이 존재하고 최소 3개 항목이 있다
- [ ] SK-04: Process 섹션이 harness-kaizen과 동일한 5단계(상태 확인→COLLECT→VERIFY→ANALYZE→PROPOSE+APPLY)를 따른다
- [ ] SK-05: 개선 대상 범위 테이블이 `flutter-toolkit/` 경로만 포함하고 `harness/` 경로를 포함하지 않는다
- [ ] SK-06: skills.sh 마켓플레이스가 COLLECT 단계의 검색 소스에 포함된다

## Script
- [ ] SC-01: `trigger-check.sh`가 실행 가능하고 exit code(0=트리거, 1=없음, 2=에러) 규칙을 따른다
- [ ] SC-02: `trigger-check.sh`가 flutter-toolkit 경로(`flutter-toolkit/evals`, `flutter-toolkit/skills`)를 기본값으로 사용한다

## Error
- [ ] ER-01: 3중 검증 게이트(GATE 1~3) 규칙이 harness-kaizen과 동일하게 유지된다
- [ ] ER-02: 게이트 우회 방지 문구("이 게이트를 우회하고 싶은 생각이 들면 멈춰라")가 포함된다

## Architecture
- [ ] AR-01: 스킬 디렉토리 구조가 `skills/flutter-kaizen/{SKILL.md, references/, scripts/, templates/}`를 따른다
- [ ] AR-02: 카이젠 docs가 기존 `docs/kaizen/` 하위에 `flutter-` prefix로 생성된다 (`flutter-research-log.md`, `flutter-changelog.md`)
- [ ] AR-03: 브랜치/커밋 prefix가 `flutter-kaizen/`, `flutter-kaizen:`으로 harness-kaizen과 구분된다
- [ ] AR-04: `search-sources.md`에 Flutter/Dart 도메인 특화 소스(flutter.dev, pub.dev, dart.dev)가 정의된다

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다
- [ ] AP-02: force push 금지

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
