# C2 계약 · 평가 가이드 묶음 — 다음 카이젠으로 넘김 (2026-09-26)

핸드오프 `.harness/handoff/2026-09-26-0110.md` §C2 는 「양이 크면 다음 카이젠(`/kaizen`)의 입력으로 넘겨도 된다」 고 했다. 전부 계약 스키마 · 설계 가이드 · 평가 가이드에 새 규칙이나 새 절을 넣는 일이라 다음 카이젠 Phase 1 ~ 4 에서 한다.

0924 처리 배정표(`.claude/kaizen-input/insights-report.md`)에는 행을 더하지 않았다. 그 표는 Phase 행 일흔넷을 닫은 표이고, 마감 검사(`check-insights-tracking.py --final`)가 계약 · QA 빈칸을 잡는다. 받을 곳은 원래 기록 `.harness/.meta/kaizen-0924/f1-harness-followups-notes.md` §다음 사이클 메모 에 이미 있다 — 다음 카이젠은 그 표와 이 파일을 함께 읽는다.

## 넘기는 것

| ID | 항목 | 받을 곳 |
| --- | --- | --- |
| F1H-35 | `feedback-schema.yaml` 체크리스트 true 뜻 · 새 키 둘 | Phase 2 · 3 |
| F1H-37 | 개정 번호 규칙 · 열 번호 정규식 · 측정 묶음 관례 · 도우미 추출 스크립트 · 봉인 둘째 줄 · `mktemp` 폴더 · 측정 공통 정의 예시 · 검사기가 돈 줄 · 추적 규칙 표 | Phase 1 · 2 · 4 |
| F1H-38 | §3.7 ①~④ 생성 측 짝 · 스키마 ①~④ 계약 측 짝 | Phase 1 · 2 |
| F1H-39 | `.harness/feedback-draft.yaml` 고정 이름 · sprint-contract Step 9 문구(`HARNESS_CONTRACT` 를 넘겨야 `contract_path` 가 채워진다) | Phase 2 — 다른 세션(`f5b7f3a5…`)의 대기 과제 3 번과 같다. 그 세션이 먼저 하면 뺀다 |
| F1H-40 | `# sprint-scope` · agent 가이드 `:79` · create-agent `:25` · create-skill `:27` · Step 6.7 (a) · V6 범위 | Phase 4. V6 · V10 범위는 다른 세션의 V10 가지(`feat/v10-fence-commonmark`)가 합쳐진 뒤 |
| F1H-43 | 세 화면 규약의 공통 규칙 원문 절을 skill 가이드에 | Phase 1 |
| F1H-80 | 근거 재조회 항목 · 오류 문구 짝 · `omitClaudeMd` · 문장 삭제 사본 검토 절차 · 평가 가이드 「12 개 이상의 편향」 | Phase 1 · 3 (근거 파일 재조회가 먼저) |
| 제안 | 풀어 둔 판에서 `validate-doc-contracts.py` 는 git init 한 사본에서 돌리라는 한 줄을 contract-schema 측정 예시에 | Phase 2 |
| 제안 | 계약마다 되풀이되는 측정 도우미 · 공통 정의 블록을 harness 공용 측정 파일로 | Phase 2 · 4 |

## 이번에 넘기지 않고 처리하는 것

사용자 결정(2026-09-26, 이 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 C4 질문)으로 바로 처리한다.

| ID | 결정 | 처리 묶음 |
| --- | --- | --- |
| F1H-41 | 폐기 결정 기록 자리는 plan-prd 「Non-goals (폐기한 결정 포함)」 표 하나 | `after-0924-discard-decisions` (워크트리 `ak-c4d`) |
| F1H-47 · F1H-48 | 킷 reviewer 일곱의 미검증 규칙을 평가 가이드 새 판으로, infra-kaizen Gotcha 8 복제 문구 포함 | `after-0924-reviewer-unverified` (워크트리 `ak-c4b`) |
