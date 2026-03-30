---
feature: "kaizen-final: 전체 정합성 (Phase 2 보완 포함)"
created: "2026-03-30 21:00"
complexity: "중간"
conditions: 14
---

## Skill
- [ ] FN-01: Phase 1 '계획-실행 분리' 패턴이 create-agent의 디자인 패턴 목록에 반영되었다 (6가지)
- [ ] FN-02: Phase 1 'Model Routing'이 create-agent의 참조 섹션에 반영되었다
- [ ] FN-03: Phase 1 '크로스 플랫폼 호환'이 create-skill의 참조 섹션에 반영되었다
- [ ] FN-04: qa-evaluator description에 비트리거 조건이 추가되었다
- [ ] FN-05: flutter-test Gotchas가 6개 이상이다 (QA 피드백 반영)
- [ ] FN-06: Phase 1~3 변경 간 크로스 Phase 충돌이 없다

## Architecture
- [ ] AR-01: 커밋이 kaizen-phase{N} prefix를 따른다
- [ ] AR-02: Phase 순서가 Phase 1 → Phase 2 → Phase 3 순서로 실행되었다

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
