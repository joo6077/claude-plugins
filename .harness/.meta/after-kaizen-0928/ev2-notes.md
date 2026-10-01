# ev2 — 평가 실행기 항목 모양 기록

- 계약: `.harness/sprint-contract-after-1001-eval-item-shape.md` (20 조건, 봉인 지문 `sha256:e1ba8785808ab308` · 측정 지문 `sha256:4c1e26738fe00e0c`)
- 가지 `chore/ak3-ev2`, 시작 판 `b33ed94a`
- 출처: `fin-notes.md` 「QA 판정과 독립 검토」 1 번 — 평가 파일 안 목록 모양이 깨지면 두 실행기가 파이썬 오류 추적을 찍고 1 로 끝났다

## 항목별 결과

| 항목 | 처리 | 커밋 |
| --- | --- | --- |
| 계약 봉인 (계약 파일 하나) | 6.5 재통과 뒤 봉인. `SEAL_OK` · `MEASURE_OK` | `c2892771` |
| 측정 도우미 | 봉인 전 지문 `98ee7757ba3a65ba` 그대로 커밋 | `7ff2158e` |
| 목록 값이 목록이 아니거나 항목이 객체가 아님 | `run-evals.py` · `sync-evals.py` 가 경로 · 몇 번째 항목 · 까닭을 한 줄로 찍고, 그 킷을 못 읽은 킷으로 센 뒤 나머지 킷을 끝까지 재고 2 로 끝낸다 | `ec444174` |
| 항목 모양 기준 | 허용 목록 — 레포 평가 파일 9 킷 122 항목을 센 열쇠 아홉과 assertions 칸 모양 둘만 통과. 모르는 열쇠(오타 `promt`)도 구조 오류다 | `ec444174` |
| 시험 | `test-run-evals.py` 경우 21 ~ 33, `test-sync-evals.py` 경우 16 ~ 28 을 더했다. 반복 줄은 표에서 만들어 낸다 | `ec444174` |
| CI 단계 이름 | `서른세 경우` · `스물여덟 경우` · `항목 모양` | `9e1aeaee` |

허용 목록은 두 실행기에 각자 두었다. 두 파일이 이미 `JSON_KINDS` · `UNREADABLE` 을 따로 들고 있고, `sync-evals.py` 는 지금 pyyaml 없이 돈다. `plugin_utils.py` 로 모으면 그 의존이 새로 생기고 시험 사본 절차도 바뀐다.

## 자기 측정 (W, `npm ci` 뒤)

| 조건 | 값 |
| --- | --- |
| 스크립트-01 | `cases=27 right=27 ok=1` · 0 |
| 스크립트-01-base | `cases=87 base_right=0 base_all_wrong=1` · 0 |
| 스크립트-02 | `cases=9 right=9 ok=1 mut_right=0 mut_ok=1` · 0 |
| 스크립트-03 | `cases=9 right=9 ok=1` · 0 |
| 스크립트-04 | run 33/33 · sync 28/28, 시작 판 실패 번호 21~30 · 16~25, 지나친 판 정상 모양 경우 모두 실패, `ci_ok=1` · 0 |
| 스크립트-05 | `census_ok=1 cases=51 right=51 ok=1` · 0 |
| 오류-01 | `cmds=11 same=11 ok=1 totals_ok=1 plain_ok=1 mut_differs=11 mut_ok=1` · 0 (`Total: 122 passed, 0 failed`) |
| 오류-02 | `cases=10 zero=10 ok=1` · 0 |
| 구조-01 · 02 | `bad=0` · `miss=[] ok=1` · 0 |
| 진단-05 | `ci-local.sh` 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0`, CI 파일에만 있는 단계 아홉 모두 0 (`174 passed` 포함) |

## tone-guide

- 1 단계: 오버레이 `.claude/tone-project.md` (어댑터 없음 · 주석 한국어) 와 코어 네 파일 · `locale-korean.md` 규칙표를 읽었다. 걸리는 규칙은 C-01 · C-07 · N-08 · S-03 · S-12 · J · K-03
- 5 단계: 새 주석 여섯 종은 이유(허용 목록의 근거 · bool 함정 · 시험 경우 뜻)만 적어 C-01 통과. `n` 은 `enumerate` 반복 번호라 N-08 대상 밖. 두 실행기의 같은 검사 몇 줄은 J(중복 구현, SHOULD)에 걸리지만 위 까닭과 계약 방침 (5)로 남겼다. 바뀐 줄의 번역투 패턴(G-1) 0 건

## 킷 버전 판단

바뀐 파일이 `scripts/` · `.github/` 뿐이라 어느 킷의 판 번호도 바뀌지 않는다. 릴리스 없음.

## 남긴 것

- `scripts/check-user-hook-copies.py` 의 레포 본 없음 오류 추적 (`fin-notes.md` 2 번) — 이번 묶음 대상이 아니다
- `target_skill` 열쇠 — 레포에서 쓰는 곳이 0 회라 허용 목록에 넣지 않았다. 쓰는 파일이 생기면 그때 넣는다
- 맨 바깥 열쇠(`skill_name` · `version` 등) 모양 검사 — 이번 대상은 목록 안 항목이라 하지 않았다
- 교차 진단은 계약 조건에 대한 지적 없이 끝났다(에이전트가 같이 넘어온 사용자 질문에 답했다). 반영할 지적이 0 건이라 조건은 그대로 봉인했다
- QA 판정 · `status: done` 은 이 묶음이 하지 않는다 → 마무리에서 처리했다 (아래)

## QA 판정과 독립 검토

- QA: APPROVE (20 조건, 실패 0 · 미검증 0). 리포트 `.harness/sprint-feedback-after-1001-eval-item-shape.md` 와 계약 `status: done` 을 `0b436fda` 로 커밋했다
- 독립 검토: 막는 결함 0 건. 막지는 않는 약점 세 가지와 QA 리포트 숫자 하나가 남았다

## 남은 것 (막지 않는 약점)

사용자가 이 약점들을 고치라고 했다. 봉인된 계약 범위 밖의 코드 변경이라 승인 뒤에 몰래 고치지 않고, 새 계약을 여는 다음 묶음으로 넘긴다.

1. `scripts/sync-evals.py:174` `get_skill_field` 의 `entry.get("target_skill")` 은 이제 닿지 않는 코드다. 허용 목록에 `target_skill` 이 없어 그 열쇠를 가진 항목은 앞에서 모르는 열쇠로 2 가 난다. 레포 사용 0 회라 의도한 선택이지만, 읽는 줄을 지우거나 허용 목록에 넣거나 둘 중 하나로 맞춰야 앞뒤가 맞는다
2. 실행기가 읽지 않는 두 번째 목록 열쇠(`evals` 가 있을 때의 `tests`)도 검사하고, `expected_output` 과 `expect` 를 같이 가진 항목도 이제 2 다. 더 엄격한 쪽이라 놓치는 것은 없다. 고칠 일이 아니라 알아둘 동작이다
3. 잘못된 UTF-8 문자가 든 평가 파일은 두 실행기 모두 `UnicodeDecodeError` 오류 추적을 찍고 죽는다 (`run-evals.py:132` · `sync-evals.py:117` 의 `read_text` 가 이 오류를 안 받는다). origin/main 판도 같아 이번에 생긴 문제는 아니지만 「한 킷이 망가져도 나머지를 잰다」는 약속에 남은 구멍이다. 못 읽은 킷 목록(`UNREADABLE`)에 넣는 쪽으로 고친다
4. QA 리포트가 「17 통과 · 3 해당 없음」 이라 쓰면서 해당 없음 조건을 넷(스킬-00 · 진단-01 · 진단-03 · 진단-04) 적었다. 판정에는 영향이 없고, 봉인된 리포트라 고치지 않는다
