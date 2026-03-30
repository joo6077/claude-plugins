---
feature: "kaizen-final: 전체 크로스 Phase 정합성"
created: "2026-03-30 20:30"
complexity: "단순"
conditions: 10
---

## Skill
- [ ] FN-01: Phase 1에서 추가된 '계획-실행 분리' 패턴이 agent-design-guide에 존재하고, Phase 2~3 변경이 이 패턴과 충돌하지 않는다
- [ ] FN-02: Phase 1에서 추가된 '크로스 플랫폼 호환' 섹션이 skill-design-guide에 존재하고, Phase 3 flutter-toolkit 스킬이 이 원칙과 충돌하지 않는다
- [ ] FN-03: Phase 3에서 생성된 flutter-test 스킬이 skill-design-guide의 아키타입(제품 검증 + 코드 스캐폴딩)에 부합한다
- [ ] FN-04: Phase 3 Gotchas 추가(flutter-audit, flutter-widget)가 Phase 1 설계 가이드의 Gotchas 작성 원칙을 따른다 (Claude가 추론만으로 알 수 없는 정보)

## Architecture
- [ ] AR-01: 전체 커밋이 kaizen-phase{N} prefix를 따른다
- [ ] AR-02: Phase 순서가 Phase 1 → Phase 2(스킵) → Phase 3 순서로 실행되었다

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
