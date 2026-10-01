# ev3 — 평가 실행기 읽기 오류 기록

- 계약: `.harness/sprint-contract-after-1001-eval-decode.md` (22 조건, 봉인 지문 `sha256:41fe586b4b54ea5f` · 측정 지문 `sha256:e9d05f9ca834ad3c`)
- 가지 `chore/ak3-ev3`, 시작 판 `9390bf96` (`chore/ak3-ev2` 끝)
- 출처: `ev2-notes.md` 「남은 것 (막지 않는 약점)」 1 번(`target_skill` 읽는 줄)과 3 번(잘못된 UTF-8 문자)

## 항목별 결과

| 항목 | 처리 | 커밋 |
| --- | --- | --- |
| 계약 봉인 (계약 파일 하나) | 교차 진단 지적을 회귀 게이트 칸에 적고 6.5 재통과 뒤 봉인. `SEAL_OK` · `MEASURE_OK` | `49fd39c3` |
| 측정 도우미 | 봉인 전 지문 `34a8b26ad31b5898` 그대로 커밋 | `66350ee6` |
| 잘못된 UTF-8 · 큰 숫자 · 깊은 중첩이 든 평가 파일 | `run-evals.py` · `sync-evals.py` 가 경로와 까닭을 한 줄로 찍고 그 킷을 못 읽은 킷으로 센 뒤 나머지 킷을 끝까지 재고 2 로 끝낸다 | `925101c3` |
| 마켓 목록을 못 읽음 (잘못된 UTF-8 · 깨진 JSON · 파일 없음) | 두 실행기가 마켓 목록 경로 한 줄을 찍고 킷을 하나도 재지 않고 2 로 끝낸다. `plugin_utils.py` 는 다른 스크립트도 써서 그대로 두었다 | `925101c3` |
| sync 의 skills 폴더를 못 읽음 | `sync-evals.py` 가 `b/skills` 경로 한 줄을 찍고 그 킷만 못 읽은 킷으로 센다 | `925101c3` |
| `target_skill` 읽는 줄 | `get_skill_field` 에서 지웠다. 허용 목록은 그대로라 그 열쇠를 가진 항목은 계속 모르는 열쇠 2 다 | `925101c3` |
| 시험 | `test-run-evals.py` 경우 34 ~ 38, `test-sync-evals.py` 경우 29 ~ 34 를 더했다. sync 시험은 잠근 폴더를 `0o755` 로 되돌린다 | `925101c3` |
| CI 단계 이름 | `서른여덟 경우` · `서른네 경우` · `잘못된 UTF-8` | `02dc31a0` |

## 자기 측정 (W, `npm ci` 뒤, 구현 커밋 `02dc31a0` 기준)

| 조건 | 값 |
| --- | --- |
| 스크립트-01 | `cases=9 right=9 ok=1` · 0 |
| 스크립트-01-base | `cases=23 base_right=0 base_all_wrong=1` · 0 |
| 스크립트-02 | `cases=3 right=3 ok=1` · 0 |
| 스크립트-03 | `cases=9 right=9 ok=1` · 0 |
| 스크립트-04 | `cases=3 right=3 ok=1 mut_right=0 mut_ok=1` · 0 |
| 스크립트-05 | run 38/38 · sync 34/34, 시작 판 실패 번호 `34,35,36,37` · `29,30,31,32,33`, 지나친 판 실패에 38 · 34 포함, `ci_ok=1` · 0 |
| 스크립트-06 | `hits=0 hits_ok=1 cases=3 right=3 ok=1` · 0 |
| 스크립트-07 | `cases=2 right=2 ok=1` · 0 |
| 오류-01 | `cmds=11 same=11 ok=1 totals_ok=1 plain_ok=1 mut_differs=11 mut_ok=1` · 0 (`Total: 122 passed, 0 failed`) |
| 오류-02 | `cases=8 zero=8 ok=1` · 0 |
| 구조-02 | `miss=[] ok=1` · 0 |
| 진단-05 | `ci-local.sh` 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0, CI 파일에만 있는 단계 아홉 모두 0 (`174 passed` 포함) |

구조-01 · 03 과 나머지 조건은 이 기록을 커밋한 뒤 잰다.

## tone-guide

- 1 단계: 오버레이 `.claude/tone-project.md` (어댑터 없음 · 주석 한국어) 와 코어 네 파일 · `locale-korean.md` 규칙표를 읽었다. 걸리는 규칙은 C-01 · C-07 · C-15 · N-08 · S-03 · S-12 · K-03 · K-11
- 5 단계: 새 주석 여섯 줄은 이유(왜 이 오류를 따로 받는지 · 받은 뒤 무엇을 하는지)만 적어 C-01 · C-15 통과. 새 이름은 `exc` · `READ_ERRORS` · `multi-good` 등 역할 이름이라 N-08 통과. 두 시험 파일이 `READ_ERRORS` 를 각자 두는 것은 기존 `BROKEN_ITEMS` 와 같은 모양이라 S-12 를 따른 것이다. 바뀐 줄의 번역투 패턴(G-1) 0 건 · `합니다`체 0 건 · 구분선 0 건

## 킷 버전 판단

바뀐 파일이 `scripts/` · `.github/` 뿐이라 어느 킷의 판 번호도 바뀌지 않는다. 릴리스 없음.

## 남긴 것

- `run-evals.py` 의 스킬 파일 확인(`exists()`)은 skills 폴더 권한이 없으면 「SKILL.md도 agent .md도 없음」 FAIL 1 을 낸다. 오류 추적으로 죽지 않고 그 킷을 실패로 세므로 동작은 막히지 않는다. 까닭 글만 어긋나서 계약 범위 밖으로 두었다
- 마켓 목록의 내용 모양(객체가 아님 · `plugins` 가 목록이 아님 · `name` 없음)은 읽기 오류가 아니라 이번에 다루지 않았다. 그런 마켓 목록은 지금도 오류 추적으로 끝난다
- `scripts/check-user-hook-copies.py` 의 레포 본 없음 오류 추적 (`fin-notes.md` 2 번) — 이번 묶음 대상이 아니다
- `remaining.md` 의 B9(킷 목록이 손으로 적은 목록)는 `dd607550` 이 이미 처리했는데 목록에 반영이 안 됐다. 그 파일은 이 묶음에서 읽기만 해서 고치지 않았다 — 다음에 목록을 고칠 때 같이 지운다
- 교차 진단이 짚은 것: 스크립트-04 의 지나친 판은 평가 파일 읽기 과잉만 잡는다. skills 폴더 · 마켓 목록을 과하게 막는 구현은 오류-01 의 열한 명령(레포 실제 마켓 목록 · skills 폴더를 읽는다)이 잡는다
- QA 판정 · `status: done` 은 이 묶음이 하지 않는다 → 마무리에서 처리했다 (아래)

## QA 판정과 독립 검토

- QA: APPROVE (22 조건, 해당 없음 넷 — 스킬-00 · 진단-01 · 진단-03 · 진단-04, 사유는 측정값 0 으로 확인). 리포트 `.harness/sprint-feedback-after-1001-eval-decode.md` 와 계약 `status: done` 을 `74a83196` 로 커밋했다. 교차 진단은 하지 않았고(`cross_diagnosis_by: pending-parent`) 질문 두 가지를 리포트에 남겼다
- 독립 검토: 막는 결함 0 건. 시험 둘은 파이썬 3.14 · 3.12.13 양쪽에서 38/38 · 34/34, ev2 판을 넣으면 새 경우(run 34 ~ 37 · sync 29 ~ 33)가 실패한다. `target_skill` 줄 삭제로 못 잡게 된 것은 없다

## 남은 것 (막지 않는 약점)

봉인된 계약 범위 밖이고, ev2 판에서도 똑같이 재현되어 이번 변경이 만든 것이 아니다. 승인 뒤에 몰래 고치지 않고 다음 묶음으로 넘긴다.

1. `sync-evals.py` 의 `discover_skills` — skills 아래 스킬 폴더 하나만 못 읽으면(권한 000) 그 스킬이 조용히 빠지고 `--check-only` 가 0 으로 통과한다. `is_dir()` 와 `(p / "SKILL.md").exists()` 가 권한 오류를 「없음」으로 삼키기 때문이다. 이번에 skills 폴더 자체는 덮었지만 한 단계 아래는 못 덮었다
2. 같은 함수 — skills 폴더 목록은 읽히는데 안으로 못 들어가면(권한 444) 오류 대신 `ORPHAN: s1` 을 낸다. `--check-only` 는 1, `--dry-run` 은 0 이고 어느 쪽도 못 읽은 킷 2 가 아니다. 1 번과 같은 자리라 같이 고친다
3. 마켓 목록 항목에 `name` 이 없으면 아직 `KeyError` 오류 추적으로 끝난다 (위 「남긴 것」 2 번과 같은 것)
