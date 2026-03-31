---
feature: "kaizen 오케스트레이터 풀런 최종 (전수 체크 보완 포함)"
created: "2026-03-30 22:00"
complexity: "복잡"
conditions: 20
---

## Skill
- [ ] SK-01: 오케스트레이터 Phase 2 ANALYZE에 "정합성 전수 체크" 단계가 필수로 포함된다
- [ ] SK-02: 오케스트레이터 Phase 3 ANALYZE에 "정합성 전수 체크" 단계가 필수로 포함된다
- [ ] SK-03: 전수 체크 단계에 결과 테이블 형식이 명시되어 있다
- [ ] SK-04: Gotchas에 "전수 체크 누락 방지" 항목이 있다
- [ ] SK-05: create-agent description에 "6가지 디자인 패턴"이 명시된다
- [ ] SK-06: create-agent Process에 Model Routing 참조가 있다
- [ ] SK-07: create-skill Process에 크로스 플랫폼 호환 참조가 있다
- [ ] SK-08: qa-evaluator description에 비트리거 조건이 있다
- [ ] SK-09: flutter-test Gotchas가 6개 이상이다

## Architecture
- [ ] AR-01: Phase 1 변경(agent-design-guide)이 Phase 2 스킬(create-agent)에 전파되었다
- [ ] AR-02: Phase 1 변경(skill-design-guide)이 Phase 2 스킬(create-skill)에 전파되었다
- [ ] AR-03: Phase 1 변경(agent-design-guide)이 Phase 2 에이전트(qa-evaluator)에 전파되었다
- [ ] AR-04: 전체 커밋이 kaizen-phase{N} 또는 kaizen: prefix를 따른다

## Error
- [ ] ER-01: 각 Phase QA REJECT 시 "최대 3회, 초과 시 중단" 정책이 Phase 1~3 모두에 명시된다

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
