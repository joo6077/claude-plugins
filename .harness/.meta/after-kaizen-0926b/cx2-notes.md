# cx2 묶음 기록 — Codex 최종 점검 지적 고침

작업 폴더 `ak2-cx2`, 가지 `chore/ak2-cx2`, 시작점 `ff28c75`. 계약 `.harness/sprint-contract-after-0926-codex-final-fixes.md`
(조건 20 · 기능 조건 11), 봉인 `sha256:26c72dfbcc4e6f88` (측정 줄 `sha256:ffe639f290b0e037`), 봉인 시각 2026-09-27 18:30.
입력은 `codex-review-2.md` 의 결함 둘이다.

## 항목별 처리

| 항목 | 처리 | 근거 · 조건 |
| --- | --- | --- |
| G5 검사가 CRLF 가이드에서 빈 칸을 통과시킴 (막아야 함) | 고침 `af18dd0` | awk 첫 규칙에서 줄 끝 `\r` 을 지운다. SK-01 · SK-02 · SK-03 · SK-05 · ER-01 |
| docs 페이지 `guide_gate` 사본 | 같은 커밋에서 고침 | SK-04 `diff_lines=0` |
| CRLF 음성 입력 | `gate_cases` 에 `blocking-empty-crlf` 1 건, 픽스처 16 줄 전부 CRLF | SK-03 `declared=12` · SK-05 |
| `design-mockup` Step 6 오기 (고치면 좋음) | 고침 `e062b70` | md · html 둘 다 Step 5. AR-01 · AR-02 |
| 교차 진단 지적 (AR-04 서명 줄) | 계약 범위 경계 절에 해소 기록 한 줄, 조건은 그대로 봉인 | 구현 커밋 서명 줄이 공통 전제와 같음을 AR-04 측정으로 확인 |
| `new-skills.md:764` · `insights-report.md:92` | 고치지 않음 | 계획 기록 / 지금 번호와 맞음 (범위 경계 절) |

## 커밋

- `afbf599` contract 봉인 (계약 파일 1 개)
- `af18dd0` fix(onboarding-kit) — SKILL.md · evals.json · 새 픽스처 · docs 페이지
- `e062b70` fix(design-kit) — visual-change-protocol md · html

## 자기 측정 (구현 커밋 뒤, 이 맥 zsh 에서)

| 조건 | 값 | 판정 |
| --- | --- | --- |
| SK-01 | bash · zsh 모두 `G5_BLOCKING FAIL rows=2 empty=1 nourl=0` · `GATE_FAIL` | 통과 |
| SK-02 | `PARITY same=18 diff=0` rc=0 | 통과 |
| SK-03 | `EVALS declared=12 ran=12 fail=0` · `EVALS_PASS` rc=0 | 통과 |
| SK-04 | `skill_lines=90 html_lines=90 diff_lines=0` | 통과 |
| SK-05 | 항목 1 개 · stack flutter · 여섯 줄 일치, 커밋된 픽스처 16 줄 중 CRLF 16 줄 | 통과 |
| ER-01 | bash · zsh 모두 `G5_BLOCKING FAIL rows=1 empty=0 nourl=1` · `GATE_FAIL` | 통과 |
| AR-01 | 1 · 1 · 1 | 통과 |
| AR-02 | 파일 4 개가 기대 집합과 같음, Step 6 0 줄 | 통과 |
| AR-03 | 6 경로가 기대 집합과 같음 | 통과 |
| AR-04 | 구현 커밋 2 개가 각각 킷 한 묶음, 마지막 줄 서명 일치, 합친 커밋 0 | 통과 |
| AR-05 | `ci-local.sh` rc=0 25 줄 + `feedback-agg-test SKIP (yq 없음)` 1 줄, 밖 4 단계 rc=0 | 통과 |
| AP-03 · AP-04 | code-fence 둘 · frontmatter rc=0 | 통과 |
| DG-02 | SKILL.md 2 + protocol md 2 = 4 (기준 4 이하), 새 픽스처 0 | 통과 |

그 밖에 `validate-plugin.py` 전체 · `sync-docs.py --check-only` · `sync-evals.py --check-only` rc=0.

tone-guide 5 단계 대조: 새 코드 줄은 awk 한 줄과 그 줄 끝 주석 하나다. 주석은 왜 지우는지만 적는다(C-01 통과). 이름 새로 만든 것 0(N 규칙 해당 없음).
구조 변경 0(S 규칙 해당 없음). 번역투 · 합니다체 0(K-02 · K-04 통과). 보존 대상 주석 삭제 0.

## 킷 버전 판단

- onboarding-kit 0.4.1 → 0.4.2 (patch). 검사 판정이 CRLF 입력에서 바뀌지만 LF 입력 판정은 같다 — 결함 고침이다.
- design-kit 0.6.0 → 0.6.1 (patch). 문서 한 문장의 번호 고침.
- 이 묶음에서는 버전을 올리지 않았다 (계약 범위 밖). 릴리스 묶음에서 올린다.

## 남은 것

- QA 판정 (qa-evaluator) · 계약 status done 전환 — 이 묶음에서 하지 않음.
- 두 킷 버전 올리기 · 릴리스 · 푸시.
