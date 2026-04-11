# Sprint Contract — Phase 4 Harness Kaizen

**작성일**: 2026-04-10
**작업자**: Phase 4 Kaizen Sub-agent
**범위**: harness README.md, create-skill/SKILL.md, init/SKILL.md (qa-evaluator.md 제외)

## 완료 조건

### [L1] 필수 (PASS 필요)

- [ ] C1: `harness/README.md` V6 bare fence 5건 모두 언어 힌트 추가 (`text`)
- [ ] C2: `harness/skills/create-skill/SKILL.md` V6 bare fence 1건 언어 힌트 추가
- [ ] C3: `harness/skills/init/SKILL.md` V6 bare fence 1건 언어 힌트 추가
- [ ] C4: `validate-plugin.py harness` 실행 시 V6 오류 7건 → 1건 이하 (qa-evaluator.md 는 Phase 3 범위이므로 제외)
- [ ] C5: Phase 3 범위 파일(`qa-evaluator.md`, `qa-evaluation-guide.md`) 미수정

### [L2] 검증 (코드 경로 확인)

- [ ] C6: `harness/README.md` 수정된 fence가 실제로 `text` 언어 힌트를 가짐 (줄 29, 65, 377, 418, 428)
- [ ] C7: `create-skill/SKILL.md` 수정된 fence가 실제로 `text` 언어 힌트를 가짐 (줄 52)
- [ ] C8: `init/SKILL.md` 수정된 fence가 실제로 `text` 언어 힌트를 가짐 (줄 60)

### [L3] 부작용 없음

- [ ] C9: V1~V5, V7 항목은 수정 전과 동일 (regression 없음)

## 제외 조건

- qa-evaluator.md V5/V6 이슈는 Phase 3 소유. Phase 4 범위 아님 — 평가 제외

## 완료 기준 요약

C1~C9 전부 PASS → APPROVE
