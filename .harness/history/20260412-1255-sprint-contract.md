---
feature: "전체 생태계 5성 Gap 개선 (QA 검증 기준)"
created: "2026-04-12 12:55"
complexity: "복잡"
conditions: 42
---

# Sprint Contract — 전체 생태계 5성 Gap 개선

## Context

QA 자체 검증으로 발견된 전 영역 gap을 개선한다:
- A) 7킷: evals + Gotchas + 템플릿 + 리서치
- B) .claude/skills/: 13개 스킬 Gotchas 0개 → 보강
- C) scripts/: release.sh --help 추가
- D) 훅: validate-plugin PostToolUse 연동

## 영향 범위

**신규 생성:**
- `harness/evals/evals.json`
- `backend-kit/evals/evals.json`
- `infra-kit/evals/evals.json`
- `rust-kit/templates/` (다수 파일)
- `design-kit/templates/` (추가 파일)

**수정:**
- `harness/skills/*/SKILL.md` (Gotchas 보강)
- `backend-kit/skills/*/SKILL.md` (Gotchas 보강)
- `infra-kit/skills/*/SKILL.md` (Gotchas 보강)
- `rust-kit/skills/*/SKILL.md` (Gotchas 보강)
- `react-kit/evals/evals.json` (내용 채우기)
- `docs/flutter/*.md` (리서치 확충)
- `.claude/skills/*/SKILL.md` (Gotchas 보강)
- `.claude/settings.json` (훅 추가)
- `scripts/release.sh` (--help 추가)

**수정 금지:**
- plugin.json 버전, marketplace.json
- .harness/project.yaml
- 기존 Gotchas 항목 순서/내용 (append-only)
- 기존 docs 내용 삭제 (보강만)

## Skill

- [ ] SK-01: `harness/evals/evals.json` 존재, 7개 스킬 전체 커버 (≥7 entries)
- [ ] SK-02: `backend-kit/evals/evals.json` 존재, 3개 스킬 전체 커버 (≥3 entries)
- [ ] SK-03: `infra-kit/evals/evals.json` 존재, 3개 스킬 전체 커버 (≥3 entries)
- [ ] SK-04: `react-kit/evals/evals.json`의 tests 배열 ≥21 entries (현재 0)
- [ ] SK-05: harness 스킬 Gotchas 평균 ≥10개 (현재 7.2)
- [ ] SK-06: backend-kit 스킬 Gotchas 평균 ≥8개 (현재 4.3)
- [ ] SK-07: infra-kit 스킬 Gotchas 평균 ≥8개 (현재 4.0)
- [ ] SK-08: rust-kit 스킬 Gotchas 평균 ≥10개 (현재 7.7)
- [ ] SK-09: `.claude/skills/` 14개 스킬 중 Gotchas 0개인 스킬이 0개 (현재 13개가 0)
- [ ] SK-10: `.claude/skills/` Gotchas 보유 스킬의 평균 ≥5개
- [ ] SK-11: 모든 신규 evals.json이 flutter-toolkit evals.json과 동일 스키마

## Script

- [ ] SC-01: `python3 scripts/validate-plugin.py` exit 0 (7 OK)
- [ ] SC-02: `python3 scripts/sync-docs.py --check-only` drift 없음
- [ ] SC-03: `scripts/release.sh --help` 실행 시 usage 출력 + exit 0
- [ ] SC-04: 모든 신규 JSON 파일 `python3 -m json.tool` 통과

## Error

- [ ] ER-01: 추가된 Gotchas 항목이 "~하지 마라/금지/하면 안 된다" 등 명확한 지시 형태 (모호한 "주의하라" 0개)
- [ ] ER-02: 추가된 Gotchas가 구체적 실수 시나리오 기술 (일반론 아닌 "X할 때 Y하면 Z된다" 패턴)

## Architecture

- [ ] AR-01: `rust-kit/templates/` ≥5개 파일 (init, api, model, service, feature 커버)
- [ ] AR-02: `design-kit/templates/` ≥8개 파일 (현재 5 → 8+, 기존과 중복 금지)
- [ ] AR-03: `docs/flutter/` 총 라인 ≥1500줄 (현재 695)
- [ ] AR-04: `docs/flutter/` 확충 문서에 출처 URL 최소 1개/파일
- [ ] AR-05: rust-kit 템플릿이 해당 스킬 SKILL.md에서 참조됨 (경로 언급)
- [ ] AR-06: `.claude/settings.json` PostToolUse에 validate-plugin 검증 훅 추가

## Anti-patterns

- [ ] AP-03: 모든 신규/수정 .md 파일에 bare code fence 0개
- [ ] AP-04: 모든 신규/수정 SKILL.md frontmatter에 name 필드 존재

## Reusability

- [ ] RE-01: 공유 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: evals.json 스키마를 기존 것에서 재사용했다

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py` 워닝 0개
- [ ] DG-02: 신규 JSON 파일 파싱 에러 0개
- [ ] DG-03: `python3 scripts/sync-evals.py --check-only` orphan 0개
- [ ] DG-04: 수정된 SKILL.md frontmatter 스키마 유지 (name, description, user-invocable)

## NFR

- [ ] NFR-01: 기존 Gotchas 항목 순서/내용 미변경 (append-only)
- [ ] NFR-02: docs/flutter/ 기존 내용 미삭제 (보강만)
- [ ] NFR-03: evals.json 내 각 항목 고유 id (중복 0)
- [ ] NFR-04: .claude/skills/ Gotchas 추가가 해당 스킬의 실제 동작과 관련있다 (다른 스킬 Gotchas 복붙 금지)
- [ ] NFR-05: validate-plugin 훅 timeout ≤ 10000ms
