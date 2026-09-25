# 카이젠 2026-09-24 Phase 3 (evaluator) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p03-evaluator.md` (조건 28 · 기능 조건 18, 봉인 `sha256:5d66862766e261e9` · `locked_at` 2026-09-24 23:59)
- 개정: `.harness/sprint-amendments-kaizen-0924-p03-evaluator.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase3-review.md` (1 회차 CHANGES 막는 이유 넷 · 권고 아홉은 초안이 반영, 2 회차 APPROVE 권고 셋은 BUILD 가 봉인 전에 반영)
- 시작 커밋 `165c8d5dd9f81bd3485de04088494ebe62012fef`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T000307-de8c7935-80054.yaml` (`verify-feedback.sh` PASS)

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `4c6b7d2` | 봉인 커밋 | 계약 1 개 |
| `c646472` | 구현 — 다섯 파일 | `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md` · evaluator-kaizen 회귀 fixture 셋 |
| `f27baee` | 개정 파일에 `end_sha` (`c646472`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p03-evaluator` 줄이 있다. 계약의 `mine()` 과 AR-06 ① 이 이 줄로
이 Phase 커밋을 가린다. **FIX 가 커밋을 더할 때도 이 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

28 조건 측정은 계약 코드 블록을 기계로 떼어 낸 묶음으로 돌렸다 — 스크래치 `p3build/extract.py`(봉인 커밋 판 계약에서
`defs.sh` · `dg07.py` · `fence.py` · `new-warnings.sh` · `ka-del.sh` 를 뗀다) · `p3build/r3.sh`(조건 문구 그대로의 측정).
QA 가 같은 묶음을 다시 돌릴 수 있다.

## 바꾼 파일

- `harness/agents/qa-evaluator.md` — 규칙 10 뒤 문단 둘(산출물이 검사일 때 다섯 가지 · 0 기대 측정의 매치 줄 가르기),
  Step 1.5 6 항(표준형 5 요소 · 커밋 구간 상태 전제), Step 2 삭제 열거, Step 3.5 10 항, 리포트 틀(`Evaluated` 는 `date` 출력 ·
  `Deletions` · `Check Artifacts` · 교차 진단 둘째 질문), Step 7 3 항, Red Flags 두 줄, References 의 옛 버전 표기.
  frontmatter 는 그대로 — harness README AUTO 구간 변화 없음
- `harness/docs/guides/qa-evaluation-guide.md` v5.0 → v5.1 — 새 절 §삭제 열거, §Evidence Validity Gate 안 새 소절 둘,
  Enforcement 표 세 행, Binary Decidability 6 항, 교차 진단 핵심 질문, Recurring Improvement Escalation 예시, References,
  Parity Table 16 행, §버전 정보
- `harness/evals/kaizen/evaluator-kaizen/assertions.json` · `expected-improvements.md` · `fixture-feedback-data/silent-check.yaml`(새 파일)

판정 임계 · 두 Canonical 절 · 카운팅 임계는 글자 그대로다(AR-05 `same:12 same:40 same:62 same:82 rule2-same`). kit reviewer
6 종에 전파할 것이 없다.

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `harness:P04` | 평가자 규칙 10 · 가이드 §산출물이 검사일 때 — 평가자가 임시 사본으로 돌리는 다섯 가지와 리포트 `Check Artifacts` 블록, Step 3.5 10 항 |
| `user-setup:P4` | 앞 세 줄은 `harness:P04` 와 한 벌로 합쳤다. 넷째 줄(삭제 열거)은 평가자 Step 2 · 가이드 §삭제 열거 · 리포트 `Deletions` 블록 |
| `F16` | 다섯 가지 ①~③ 과 회귀 fixture `silent-check`. 킷별 실제 결함은 각 Phase 몫(bambu:P2~P4 · other-kits:P2 · P3 · P5) |
| `F31` | 측정 스크립트 부분 — ⑤ 알려진 답 · 교차 진단 둘째 질문 · 삭제 목록 |
| `harness:P08` | 평가자 리포트 틀의 `Evaluated` 를 `date '+%Y-%m-%d %H:%M'` 출력으로 (계약 쪽은 Phase 2) |
| `메타 이슈 3` | 러닝북 Phase 3 과제 — 가이드 §0 이 기대값인데 매치가 나올 때 · 평가자 규칙 10 문단 · Red Flags. 판정은 계약 측정 그대로, 낱말 필터 금지, 좁힌 측정은 두 값과 함께 |

Phase 2 넘김 표 9 행도 전부 반영했다(평가자 `:590` · `:1217`, 가이드 `:12` · `:742-743` · `:746` · `:1785` · `:1862` · `:1915` · `Evaluated`).
Phase 2 가 넘긴 확인 목록(보조 스크립트가 `경로:13:8` 의 열 번호를 줄 번호로 읽음)은 ⑤ 의 예로 들어갔다. 카이젠 Step 7 에서
찾은 죽은 회귀 패턴(`vacuous-zero` 둘째 패턴 `Agent\(general-purpose\)`, 2026-09-22 부터 0 건)은 `cross_diagnosis_by: pending-parent` 로 바꿨다.

## 미반영 키와 사유

- `F31` 의 UI 관례 대조 부분 — 행 비고대로 Phase 5 `flutter:P-INSPECTOR-convention` 몫이다
- 근거 파일 §4 권장안 11(범위 밖 삭제는 FAIL) — 평가자는 계약에 없는 요구를 만들지 않으므로 「사용자 확인 필요」 로 올리게 했다. 계약에 범위 조건이 있으면 그 조건이 FAIL 을 낸다

## 넘기는 것 (명시적 미완)

| 대상 | 누가 | 할 일 |
| --- | --- | --- |
| `skill-design-guide.md §3.7 ①~④` | 다음 사이클 Phase 1 | 다섯 가지 ①~④ 의 생성 측 짝이 없다(⑤ 만 §3.7 에 있다) |
| `contract-schema.md ①~④` | 다음 사이클 Phase 2 | 같은 ①~④ 의 계약 측 짝 — 산출물이 검사인 조건에 어떤 사본 대조를 적게 할지 |
| `assertions.json 실행기` | Phase 4 | contract-kaizen · evaluator-kaizen 두 벌을 도는 실행기가 없다. 그래서 죽은 패턴이 이틀 동안 0 건이었다. `scripts/` 에 둘지 Phase 4 가 정한다 |
| `.github/workflows/ci.yml` | Final | 위 실행기가 생기면 그 실행 명령 한 줄을 CI 단계에 넣는다. 실행기가 없으면 넣을 줄이 없다 |
| `docs/harness/qa-evaluation-guide.html` | Final F2 | 가이드 v5.1 로 다시 만든다. `validate-post-kaizen.py --since 165c8d5` 의 `docs-site-regen` 이 이 때문에 FAIL 이다 |
| `harness/skills/sprint/SKILL.md:118` | 확인만 | 교차 진단 질문 수가 둘 그대로라 「물을 두 가지」 가 맞다. 고칠 것 없음 |

Final 이 더 할 것: `harness` plugin.json 버전 — evaluator-kaizen 버전 판단표로는 「검증 레벨/루브릭 변경」 이라 minor 다
(리포트에 새 블록 둘 · self-check 10 항). 이 Phase 는 공유 파일(marketplace · plugin.json · 루트 README · 루트 CLAUDE.md ·
`docs/kaizen/*.md` · 감사 로그 · 실패 횟수 파일 · 처리 배정표)을 건드리지 않았다. evaluator-kaizen Step 7 의
`kaizen-phase-3-pre` 태그는 만들지 않았다 — 되돌릴 기준점은 봉인 커밋 `4c6b7d2` 다.

## changelog 한 단락

평가 가이드를 v5.1 로 올렸다. 스프린트가 만든 것이 검사 스크립트 · 막는 훅 · 새 시험 파일이면, 원본에서 나온 「위반 0」 은
그 검사가 살아 있다는 증거가 아니다. 평가자는 임시 사본으로 다섯 가지(첫 칸만 읽기 · 표에만 올린 시험 · 한 칸 못 읽으면
전체 꺼짐 · 셸마다 다른 대상 수 · 효과 증명)를 돌리고 리포트 `Check Artifacts` 블록에 남긴다. 금지 낱말을 세는 측정에 매치가
나오면 줄마다 가르되 낱말 필터로 빼지 않고, 판정은 계약 측정 그대로 둔다. 구현 판정마다 지운 파일을 뽑아 `Deletions` 블록에
올리고, 재는 조건이 없으면 FAIL 이 아니라 사용자 확인으로 넘긴다. 스키마 v5.5 와 표기를 맞췄다(Diff-Scope 표준형 5 요소 ·
커밋 구간 상태 전제 · Parity 16 행), 평가 시각은 `date` 출력을 옮긴다. evaluator-kaizen 회귀 확인의 죽은 패턴을 바꾸고
`silent-check` fixture 를 더했다.

## 킷 로그 한 단락 (harness)

2026-09-24 Phase 3 — qa-evaluation-guide v5.1. 트리거 orchestrator-phase-3. 피드백: 글로벌 평가 피드백 최근 30 건(APPROVE 26 ·
REJECT 4) + `grep` 으로 찾은 네 건(2026-09-23 · 2026-09-24). 근거:
[MITRE CWE-20](https://cwe.mitre.org/data/definitions/20.html) (빠진 입력 · 남는 입력까지 관련 속성 전부 검사 — ①),
[MITRE CWE-754](https://cwe.mitre.org/data/definitions/754.html) (예외 조건 하나를 잘못 다뤄 예상 밖 상태 — ③),
[pytest Exit Codes](https://docs.pytest.org/en/stable/reference/exit-codes.html) (수집 0 건은 종료 코드 5 — ②),
[zsh Parameter Expansion](https://zsh.sourceforge.io/Doc/Release/Expansion.html) (`SH_WORD_SPLIT` 이 꺼진 기본값 — ④),
[git diff](https://git-scm.com/docs/git-diff) (`--name-status` 의 `D` — 삭제 열거),
[CheckEval](https://arxiv.org/abs/2403.18771) (판정을 추적 가능한 yes/no 로 — 한계 문단). 근거 파일이 밝힌 한계 — 사본 절차
셋을 그대로 규정한 1 차 출처는 없다(레포 규칙으로 옮긴 추론), 모든 칸을 읽어야 안전한 검사는 실패로 닫는 쪽이 옳을 수 있다(③
에 분기로 넣음), 이름을 찍지 않는 러너가 있다(② 에 수집 명령의 시험 수를 대안으로 넣음).

## 다음 사이클 메모

- 가이드 `:132` 「12 개 이상의 편향」 수치는 이번 근거 파일로 재확인되지 않았다 — 고치지 않았다
- Phase 1 notes 가 제안한 「문장 삭제 사본으로 문서 조건의 판별력을 재는 검토 절차」 — 처리 배정표 밖이라 이번에 넣지 않았다.
  이 계약은 초안 단계에서 그 절차를 48 사본으로 돌렸다
- 카이젠 Gotcha 「L3 Coverage Honesty 회귀 체크」 실측 — 글로벌 평가 피드백 최근 10 건(파일 이름 시각 순, 2026-09-24T175139 ~ T223853)
  가운데 `샘플링-` 태그가 든 것 0 건. 전수 검증을 주장했는데 일부만 본 태그 누락인지는 파일만으로 못 가른다
- 「이 구간을 바꾸지 않는다」 조건을 지운 줄 수로만 재면 줄을 더해 판정을 느슨하게 만드는 편집이 통과한다(2 회차 검토).
  이 계약은 더한 줄의 자리 · 수까지 잠갔다. contract-schema 조건 패턴에 올릴지 다음 사이클 Phase 2 가 본다
- 계약 피드백 저장에서 `project_name` 이 워크트리 이름 `kaizen-0924` 로 적혔다 — Phase 2 notes 와 같은 결함(Phase 4 · 12 몫)
- 피드백 초안 파일 `.harness/feedback-draft.yaml` 을 여러 Phase 가 같은 이름으로 쓰면 서로 덮는다 — 이번에는 `.harness/feedback-draft-p03.yaml` 로
  이름을 갈라 썼다(`save-feedback.sh` 가 저장 뒤 지운다). sprint-contract Step 9 의 고정 이름을 Phase 4 가 볼 만하다
