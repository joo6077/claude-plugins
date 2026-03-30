---
feature: "kaizen-orchestrator 최종 (리서치 소스 확장 + QA 보강)"
created: "2026-03-30 18:30"
complexity: "중간"
conditions: 22
---

## Skill
- [ ] SK-01: `SKILL.md`에 YAML frontmatter(name, description, argument-hint, user-invocable)가 있다
- [ ] SK-02: description에 트리거 키워드와 비트리거 조건이 포함된다
- [ ] SK-03: Gotchas 섹션이 존재하고 최소 3개 항목이 있다
- [ ] SK-04: Process가 Step 0→1→2→3→4→5 순서를 따른다
- [ ] SK-05: 각 Phase(Step 1~3)에 ANALYZE → Sprint Contract → APPLY → QA Evaluator 4단계가 모두 포함된다
- [ ] SK-06: 각 Phase의 QA REJECT 시 "최대 3회, 초과 시 중단하고 사용자 알림" 정책이 Step 1~3 모두에 명시된다
- [ ] SK-07: Final(Step 4)에 크로스 Phase 정합성 조건이 명시되어 있다

## Architecture
- [ ] AR-01: 디렉토리 구조가 `.claude/skills/kaizen-orchestrator/{SKILL.md, references/}`를 따른다
- [ ] AR-02: `references/phase-dependencies.md`에 Phase 간 의존성 맵이 정의되어 있다
- [ ] AR-03: `references/search-sources.md`에 Phase 1 전용 리서치 소스가 정의되어 있다
- [ ] AR-04: Phase 순서가 설계 가이드(1) → harness(2) → flutter-toolkit(3) → Final이다

## Script
- [ ] SC-01: harness-kaizen의 cron이 "직접 cron 없음"으로 오케스트레이터에 위임되었다
- [ ] SC-02: flutter-kaizen의 cron이 "직접 cron 없음"으로 오케스트레이터에 위임되었다

## Error
- [ ] ER-01: Phase 스킵 규칙(개선 포인트 0개 시)이 정의되어 있다
- [ ] ER-02: 모든 Phase 스킵 시 종료 정책(PR 생성 안 함)이 정의되어 있다

## Research
- [ ] RS-01: search-sources.md에 Anthropic 공식 소스가 포함된다
- [ ] RS-02: search-sources.md에 경쟁사 공식 소스(OpenAI, Google, Microsoft)가 포함된다
- [ ] RS-03: search-sources.md에 AI 트렌드 키워드(reasoning model, MCP, agentic RAG 등)가 포함된다
- [ ] RS-04: Step 0에서 3개 소스(Phase 1 + harness + flutter)를 합쳐 리서치하도록 명시된다

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
