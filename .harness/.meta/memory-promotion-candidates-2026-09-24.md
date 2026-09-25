# 메모리 승격 후보 — kaizen-2026-09-24

오케스트레이터 Step F3.5 산출물. 이번 사이클 Phase QA 판정과 Final 교차 진단 지적을 근본 원인 단위로 묶었다. 카이젠은 후보만 낸다 —
승격 여부 · 자리 · 등급은 `/reflect-promote` 가 사용자 승인을 거쳐 정한다. 승격 원장과 메모리 파일은 쓰지 않았다.

근거는 모두 기계 신호(QA 리포트 · 교차 진단 결과를 옮긴 전역 피드백 · 명령 출력)라 `grounding` 이 `execution_evidence` 다. 자기추론뿐인 후보는 내지 않았다.
이 파일은 이번 사이클 데이터 풀의 입력이 아니다 — 같은 사이클 안에서 왕복시키지 않는다.

```yaml
# kaizen-memory-candidates
cycle_id: kaizen-2026-09-24
generated_at: "2026-09-25T22:36:29+09:00"
candidates:
  - canonical_tag: lint-new-warning-added-lines-only
    grounding: execution_evidence
    actionability: claude_behavior
    scope: project
    risk_class: medium
    procedurality: single_rule
    enforcement_need: soft_reminder
    user_stated_constraint: false
    freq: 4
    undesired_behavior: "편집기 경고를 더한 줄에서만 세어, 새 소제목이 옛 소제목과 겹쳐 손대지 않은 옛 줄에 붙은 같은 제목 경고(MD024)를 놓친다 — Phase 7 · 8 · 9 · 11 측정이 0 을 냈다"
    desired_behavior: "파일마다 (규칙, 그 줄 글자) 묶음을 편집 전 판과 비교해 새 묶음을 센다. 기록 파일에 새 항목을 넣을 때는 소제목에 날짜를 붙인다"
    source_evidence:
      - path: ~/.harness/feedback/contract/5a24cc99-2026-09-25T060812-de8c7935-70385.yaml
        anchor: "Final 교차 진단 (xdiag-all.md P7) — DG-02"
      - path: ~/.harness/feedback/contract/5a24cc99-2026-09-25T074456-de8c7935-5544.yaml
        anchor: "Final 교차 진단 (xdiag-all.md P8) — DG-02"
      - path: .harness/sprint-amendments-kaizen-0924-p09-rust-kit.md
        anchor: "교차 진단 뒤 Final 에서 고침"
      - path: .harness/sprint-amendments-kaizen-0924-p11-planning-kit.md
        anchor: "교차 진단 뒤 Final 에서 고침"
    draft_rule: "새 편집기 경고는 더한 줄만 세지 말고 파일마다 규칙 + 줄 글자 묶음을 편집 전 판과 비교한다"
  - canonical_tag: scope-count-signed-commits-only
    grounding: execution_evidence
    actionability: claude_behavior
    scope: project
    risk_class: medium
    procedurality: single_rule
    enforcement_need: soft_reminder
    user_stated_constraint: false
    freq: 6
    undesired_behavior: "건드리면 안 되는 파일 · 다른 킷 폴더를 서명 줄이 달린 커밋 목록으로만 재서, 서명을 빠뜨린 커밋이 그 파일을 고쳐도 측정이 0 을 낸다 — Phase 2 · 7 · 8 · 11 · 12 · 14 교차 진단이 사본으로 재현"
    desired_behavior: "금지 경로는 git log <기준>..<상한> -- <경로> 로 서명과 상관없이 커밋 수를 직접 세고, 서명 없는 커밋 수를 따로 낸다"
    source_evidence:
      - path: ~/.harness/feedback/contract/5a24cc99-2026-09-24T222231-de8c7935-60429.yaml
        anchor: "Final 교차 진단 (xdiag-all.md P2) — ER-03 둘째 · AR-06"
      - path: ~/.harness/feedback/contract/5a24cc99-2026-09-25T091602-de8c7935-34207.yaml
        anchor: "Final 교차 진단 (xdiag-all.md P11) — ER-03 (d) · AR-01 ①"
      - path: ~/.harness/feedback/contract/5a24cc99-2026-09-25T110416-de8c7935-62800.yaml
        anchor: "Final 교차 진단 (xdiag-all.md P14) — ER-03 (d) · AR-01 ①"
    draft_rule: "범위 측정은 서명 줄 커밋 목록 대신 git log <기준>..<상한> -- <경로> 로 직접 센다"
  - canonical_tag: qa-report-summary-count-typed
    grounding: execution_evidence
    actionability: claude_behavior
    scope: project
    risk_class: low
    procedurality: single_rule
    enforcement_need: soft_reminder
    user_stated_constraint: false
    freq: 5
    undesired_behavior: "QA 리포트 요약 수(N/A 건수 · end_sha 줄 수 · 측정 수)를 손으로 적어 본문 나열과 어긋난다 — Phase 4 · 6 · 7 · 10 · 14"
    desired_behavior: "요약 수는 본문 표 · 목록을 다시 세어 적거나 명령 출력(grep -c 등)을 옮긴다"
    source_evidence:
      - path: .harness/sprint-feedback-kaizen-0924-p04-harness.md
        anchor: "### Diagnostics (6/6, N/A 3 포함) — 실제 N/A 는 넷(SC-00 · DG-01 · DG-03 · DG-04)"
      - path: ~/.harness/feedback/evaluator/5a24cc99-2026-09-25T044043-de8c7935-36068.yaml
        anchor: "Final 교차 진단 (xdiag-all.md P4) — N/A 3 건(실제 4)"
      - path: ~/.harness/feedback/evaluator/1a3bcba6-2026-09-25T062632-de8c7935-88430.yaml
        anchor: "Final 교차 진단 (xdiag-all.md P6) — N/A 3 건(실제 4)"
      - path: ~/.harness/feedback/evaluator/5a24cc99-2026-09-25T111453-de8c7935-47034.yaml
        anchor: "Final 교차 진단 (xdiag-all.md P14) — 측정 수 26 vs 25"
    draft_rule: "QA 리포트의 요약 수는 손으로 쓰지 말고 본문 목록을 다시 센 값이나 명령 출력을 옮긴다"
  - canonical_tag: cycle-state-not-advanced
    grounding: execution_evidence
    actionability: claude_behavior
    scope: project
    risk_class: medium
    procedurality: single_rule
    enforcement_need: soft_reminder
    user_stated_constraint: false
    freq: 1
    undesired_behavior: "워크플로가 Phase 를 돌려 사이클 상태 파일(kaizen-state.yaml cycle_id)이 옛 사이클로 남았고, 사후 점검의 날짜 검사 다섯이 옛 사이클 항목으로 통과했다"
    desired_behavior: "사이클을 시작할 때 kaizen-state.yaml 의 cycle_id 를 새 사이클로 바꾸고, 사후 점검 PASS 를 믿기 전에 그 값이 이번 사이클인지 확인한다"
    source_evidence:
      - path: .harness/sprint-contract-kaizen-0924-final.md
        anchor: "## 배경 — 편집 전 실측 첫째 결함"
      - path: scripts/validate-post-kaizen.py
        anchor: "cycle_state()"
    draft_rule: "사후 점검을 믿기 전에 kaizen-state.yaml 의 cycle_id 가 이번 사이클인지 확인한다"
```

다음 할 일: `/reflect-promote` 를 불러 이 파일의 후보 넷을 재판정한다. 후보 파일을 만든 것은 승격 완료가 아니다.
