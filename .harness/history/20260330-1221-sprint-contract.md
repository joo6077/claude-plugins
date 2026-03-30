---
feature: "kaizen-phase1: 설계 가이드 업데이트"
created: "2026-03-30 19:30"
complexity: "단순"
conditions: 8
---

## Guide
- [ ] GD-01: agent-design-guide.md에 Dual-Agent 패턴(계획/실행 분리)이 6번째 패턴으로 추가된다
- [ ] GD-02: agent-design-guide.md에 Model Routing(작업별 자동 모델 선택) 개념이 모델 선택 섹션에 추가된다
- [ ] GD-03: skill-design-guide.md에 크로스 플랫폼 호환성(Codex CLI SKILL.md 호환) 언급이 추가된다
- [ ] GD-04: 추가된 내용에 출처 URL이 명시된다

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
