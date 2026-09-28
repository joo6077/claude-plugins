# ex2 — 바깥 원문 대조 셋 더 반영 · routing 예시 (2026-09-28)

계약 `.harness/sprint-contract-after-0928-external-facts-2.md` (26 조건, 봉인 `sha256:30978e4d67ca2840` · 측정 `sha256:8c1c9fcbc681c2ca`, 봉인 커밋 `ce5df05`).
개정 `.harness/sprint-amendments-after-0928-external-facts-2.md` A-01 (방향 unchanged). 가지 `chore/ak3-ex2`, 기준 판 `e500a63`.

## 교차 진단 반영 (봉인 전)

- remaining.md A11 은 C-06 강도 · 663 이름표 · `__` 예시 셋이다. C-06 은 앞 묶음이 SHOULD 로 내렸지만 옛 값 전체 검색을 돌리니 `docs/tone-kit/comment-economy.html:923` 에 「원칙 6은 MUST」 표지가 남아 있었다. SK-12 로 넣고 범위 목록 · AR-03 페이지 목록에 그 페이지를 더했다 (25 → 26 조건).
- AR-01 서명 줄은 묶음 공통 전제의 값이고 구현도 같은 모델이 했다는 한 줄을 범위 경계에 적었다.

## 항목별 결과

| 항목 | 결과 | 커밋 |
| --- | --- | --- |
| X1 material-design.md 표 행 · 257 · 280 · 출처 줄 | 발표 원문 `later this year` 와 Q3 업데이트 설명으로 바꿨다. 출처는 블로그 글 두 주소와 조회일 | `48603dc` |
| X1 대응 페이지 6 절 | 머리를 `Android 16 후속 업데이트` 로, 원문 인용과 글 두 주소를 붙였다 | `cfcd634` |
| X2 evals.json `deprecation-claim-fidelity` | 출처 상태를 Firebase · Apple 로 나누고, 출처 칸에 Apple 문서 두 주소, `.p8` · 업로드 · `.p12` 판정 줄과 설명을 맞췄다 | `e7e4677` |
| X2 Firebase 갱신일 `2026-09-17` | 따르지 않음 — 계약 GAP 표대로 2026-09-28 직접 조회값 `2026-09-24` 가 맞다 | — |
| X3 locale-korean.md §2 · §3 · §4 · §10, sources.md | 치환표 · 종결형 고정 · 외래어 1번 · 3번은 이 킷의 컨벤션, 663 은 K-05 2번 원칙만 뒷받침한다고 적었다. 강도 그대로 | `9dece2e` |
| X3 korean-technical-writing.md · overview.md 와 페이지 넷 | 원칙 1 · 2 · 8 과 overview 9 절 인용을 뺐다. 원칙 4 는 참고로만, 원칙 5 는 2번 원칙으로 좁혔다. 강도 그대로 | `cfcd634` · `60dfe59` |
| R routing.md 85 · 86 · 88 · 120 행 | `__` 를 `_` 로 | `cfcd634` |
| A11 C-06 남은 표지 | `원칙 6은 SHOULD` 로 | `cfcd634` |

`60dfe59` 는 원칙 2 설명 줄 앞에 붙였던 문장을 다음 단락으로 옮긴 것이다. 원래 줄이 번역투 패턴을 예로 들고 있어서 그 줄을 고치면 ER-02 가 새로 더한 줄로 셌다 (2 건 → 0 건).

## 자기 측정 (끝 판)

- SK-01: 0 이어야 할 넷 0 · 1 이상이어야 할 넷 각 1 · 표 행 1. SK-02: 0 · 1 · 넷 각 1. SK-03: 0, 파일 두 줄.
- SK-04: `x2check.py` 출력 `OK`, JSON · run-gate-evals · sync-evals rc=0. 음성 대조: 끝 줄 `}` 를 뺀 사본에 JSON 명령 rc=1.
- SK-05: 절별 663 0 · 0 · 1 · 1 · 0, `근거로 세지 않는다` 1, `2번 원칙` 1, `국립국어원·번역투 연구 근거` 0, 강도 목록 BASE 와 같다. SK-06: 카드별 같은 값, 강도 목록 같다.
- SK-07: 여섯 값 각 1, 규칙표 강도 같다. SK-08: 여섯 값 각 1, 주소 모음 문구 1. SK-09: 0 · 1 · 1 (두 파일). SK-10: 0 · 0 · 1 · 1. SK-11: 0, 네 줄 각 1. SK-12: 0 · 1 · 1.
- SC-01: 로컬 CI 25 단계 rc=0, `feedback-agg-test SKIP (yq 없음)` 한 줄. 여섯 단계와 playwright 둘(156 · 8 통과) rc=0.
- ER-01: 0 줄 rc=0. 음성 대조는 개정 A-01 — 새 주소를 더한 떠 있는 커밋 `14d581b` 에서 1. ER-02: 0.
- AR-01: BAD 0 · 커밋 7. AR-02: 0. AR-03: CSS 링크 6 × 1, `6/6 PASS` rc=0.
- AP-03 · AP-04 rc=0. DG-01 0. DG-02: md 6 파일 경고 0 · rc=0.

## 킷 버전 판단

design-kit · onboarding-kit · tone-kit 셋이 바뀌었다. 모두 문장과 평가 데이터 정정이고 규칙 강도는 그대로라 patch 로 본다. 릴리스는 합친 뒤 main 에서 한다 (이 묶음에서는 하지 않았다).

## 남은 것

- QA 판정과 `status: done` — 이 묶음 지시상 하지 않았다.
- `docs/tone/research-log.md:43 · 44` 의 663 · C-06 줄 — 그 사이클의 기록이라 고치지 않았다 (계약 범위 경계).
- `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md:270` 과 대응 페이지의 663 행 — 이미 「근거로는 약하다」 고 적혀 원문 대조와 어긋나지 않아 그대로 뒀다.
- ER-01 음성 대조에 적힌 예시 주소가 앞 묶음 기록에 이미 있어 대조가 0 을 냈다. 개정 A-01 로 대조 주소만 바꿨다 — 다음 계약은 대조 주소를 시작 판에서 `git grep` 해 0 인지 먼저 본다.
