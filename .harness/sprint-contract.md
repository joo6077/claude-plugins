---
feature: "자동화 성숙도 5개 영역 5/5 달성 (cron 제외)"
created: "2026-04-13 00:00"
complexity: "복잡"
conditions: 20
---

# Sprint Contract — 자동화 성숙도 5/5 달성

## Context

cron(영역 1) 제외, 5개 영역(3,4,5,6,7)을 각각 5/5로 끌어올린다.

## 영역 3: Phase 실행 (3→5)

- [ ] P3-01: spawn-kaizen-phase.sh 실행 시 kaizen-state.yaml의 current_phase, status가 자동 갱신된다
- [ ] P3-02: finalize-phase.sh pass 실행 시 kaizen-state.yaml의 last_approve_timestamp가 현재 시각으로 갱신된다
- [ ] P3-03: finalize-phase.sh fail 실행 시 kaizen-state.yaml의 last_reject_timestamp가 현재 시각으로 갱신된다
- [ ] P3-04: 10개 Phase 전부 완료 후 finalize-phase.sh 10 pass 실행 시 status가 "completed"로 전환된다

## 영역 4: 산출물 동기화 (4→5)

- [ ] P4-01: .claude/settings.json PostToolUse 훅에 harness 소스 변경 시 docs-site 재생성 알림이 포함된다
- [ ] P4-02: finalize-phase.sh 완료 시 changelog 자동 append 또는 알림이 출력된다

## 영역 5: 오케스트레이터 self-improvement (4→5)

- [ ] P5-01: meta-kaizen 스킬 SKILL.md가 존재하고 user-invocable: true이다
- [ ] P5-02: meta-kaizen 스킬의 Process 섹션에 외부 리서치(WebSearch/Codex) 기반 orchestrator 개선 단계가 포함된다

## 영역 6: 품질 보증 (4→5)

- [ ] P6-01: .claude/settings.json PostToolUse 훅에 validate-plugin 자동 실행이 포함된다
- [ ] P6-02: validate-plugin 훅의 timeout이 10000ms 이하이다

## 영역 7: 안전성/복구 (4→5)

- [ ] P7-01: finalize-phase.sh fail 실행 시 auto-revert 여부를 사용자에게 안내하고, --auto-revert 플래그로 자동 revert를 지원한다
- [ ] P7-02: validate-post-kaizen.py의 scope-isolation 체크가 Phase별 파일 범위를 검증한다 (이미 존재 확인)

## Anti-patterns

- [ ] AP-01: settings.json 훅이 기존 훅을 덮어쓰지 않고 추가한다
- [ ] AP-02: auto-revert는 --auto-revert 명시 플래그 없이는 절대 실행되지 않는다

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py` 워닝 0개
- [ ] DG-02: `bash scripts/finalize-phase.sh 5 pass` exit 0
- [ ] DG-03: 성숙도 리포트 영역별 합계가 산술적으로 정확하다
