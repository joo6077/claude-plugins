# ev 묶음 기록 — 평가 실행기 둘 (대상 없는 바로가기 · 못 읽는 킷 하나)

- 계약: `.harness/sprint-contract-after-0930-eval-runners.md` (20 조건, 봉인 `conditions_digest` `680e37872c5063e7` · `measurement_digest` `6757b915845ee19d`)
- 가지 `chore/ak3-ev`, 시작 판 `fe6704d8`. push · 합치기 · QA 판정은 하지 않았다.

## 항목별 결과

| 항목 | 결과 | 커밋 |
| --- | --- | --- |
| 봉인 | 교차 진단 지적(구조-01 시작 판 값 `scope_entries=0` → 실측 `6`)을 측정 줄에 반영한 뒤 6.5 재통과 · 봉인. 봉인 커밋 파일 1 개 | `e43427d1` |
| 측정 도우미 | 봉인 전 지문 `e1d81f6a7352fe42` 그대로 커밋 | `acb09f96` |
| (1) 대상 없는 바로가기 | `run-evals.py` · `sync-evals.py` 가 대상 킷을 `os.path.lexists` 로 고른다. 가리키는 파일이 없는 바로가기는 `UNREADABLE <경로> (바로가기 대상 없음)` 줄과 종료 코드 2. 자리가 아예 없는 킷은 지금처럼 「대상 아님」 | `0831e949` |
| (2) 못 읽는 킷 하나 | 못 읽음 · 깨짐에서 바로 끝내지 않고 나머지 킷을 끝까지 잰 뒤 `못 읽은 킷 N 개: …` 를 찍고 2 로 끝난다 | `0831e949` |
| (4) 시험 | sync 경우 4 · 5 · 6, run 경우 7 · 8 · 9. 시작 판 도구로는 4 · 6 과 7 · 9, 바로가기 판정을 늘 참으로 바꾼 변이로는 5 와 8 만 실패 | `0831e949` |
| CI 이름 | 두 시험 단계 이름에 「여섯 경우」 · 「아홉 경우」 | `72c90f47` |
| (3) backend-kaizen | 10 번 항목의 「즉시 종료하는 구조 유지」 를 「나머지 킷을 끝까지 재고 못 읽은 킷 이름을 적은 뒤 2」 로. 머리말은 그대로 | `62668713` |

## 자기 측정 (W, TMPDIR 은 scratch 아래)

- 스크립트-01 `cases=3 right=3 ok=1` · 스크립트-02 `cases=6 right=6 ok=1 lexists_uses=4 mut_right=0 mut_ok=1` · 스크립트-03 `cases=9 right=9 ok=1` · 스크립트-03-base `cases=12 base_right=0 base_all_wrong=1`
- 스크립트-04 `run_ok=1 sync_ok=1 run_base_fails=7,9 sync_base_fails=4,6 run_mut_fails=8 sync_mut_fails=5 ci_ok=1`
- 오류-01 `cases=6 right=6 ok=1 absent_same=1` · 오류-02 `lines=7 same=1` · 스킬-01 `line=1 old=0 ok=1` · 구조-02 `miss=[] ok=1` · 금지-04 `found=1 same=1`
- 로컬 CI(`scripts/ci-local.sh`, `npm ci` 뒤) `steps=52 run=47 skip=5 unsupported=0 failed=0`, CI 파일에만 있는 단계 아홉 모두 종료 코드 0 (`npx playwright test` 174 passed)

## tone-guide

- 1 단계: 오버레이 `.claude/tone-project.md`(어댑터 없음 · 주석 한국어) 와 코어 네 파일 · `locale-korean.md` 를 레포 판으로 읽었다. 걸리는 규칙은 C-01 · C-07 · H(보존) · N-08 · S-03 · S-07 · K-03 · K-04.
- 5 단계: 더한 줄 186 줄에서 구분선 · fallback 이름 · 한 글자 대입 · 번역투 · 합니다체 · 자화자찬 0 건. 주석 8 줄은 모두 까닭을 적은 줄이고, 옛 판의 까닭 주석 셋(권한 · 깨짐으로 넘기면 통과한다)은 지우지 않고 남겼다.

## 킷 버전 판단

바뀐 곳이 `scripts/` · `.github/` · `.claude/` 뿐이라 킷 릴리스는 없다.

## 남긴 것

- 레포 밖 로컬 CI 도구 `.harness/handoff/2026-09-26-tools/ci-local.sh` 는 없어 레포 안 `scripts/ci-local.sh` 로 쟀다 — 도구가 CI 파일을 그때그때 읽어 CI 에만 있는 단계까지 돈다. 옛 도구를 되살릴 까닭이 없어 그대로 둔다.
- `sync-evals.py` 는 킷마다 평가 파일을 두 번 읽는다(`main` · `process_kit`). 두 번째 읽기는 첫 읽기가 된 킷에서만 돌아 이번 동작과 부딪히지 않는다 — 계약 범위 밖이라 합치지 않았다.
- 앞 end 계약 `스크립트-06` 이 적은 시험 끝 줄(6 · 3)은 이번에 9 · 6 으로 늘었다. 그 계약은 done 이고 경우를 더한 쪽이라 더 엄격하다.
- push · PR 은 이 묶음 밖이다.

## QA 판정과 독립 검토

- QA `APPROVE` — 17/17 통과, N/A 3(진단-01 · 03 · 04). 리포트와 계약 `status: done` 은 `c98e318e`.
- 설치된 harness 판(v0.16.0)의 봉인 검사 식은 한국어 조건 번호를 못 읽어 `SEAL_BROKEN` 으로 잘못 나온다. 레포 판(v0.17.0) 식으로는 `SEAL_OK`. 설치본을 새 판으로 올리면 풀린다.
- 독립 검토 막는 결함 0. 아래 다섯은 모두 시작 판에서도 똑같이 나와 이번 변경으로 나빠진 것은 아니다. 계약 범위 밖이라 고치지 않고 남긴다.
  1. `evals.json` 내용이 `null` 이면 거짓으로 통과한다. `json.loads` 가 `None` 을 돌려주는데 코드가 이를 「파일 없음」 표시와 구분하지 못한다. 「없음」과 「못 읽음」을 가르려던 이번 취지에 남은 구멍이라 다음 묶음에서 가장 먼저 볼 것.
  2. 내용이 숫자(예: `5`)이면 두 실행기 모두 오류 추적을 찍고 1 로 끝난다. 1 은 「검사 항목 실패」 뜻이라 구조 오류 2 와 섞인다.
  3. `run-evals.py` 는 항목이 0 개인 파일(`{"evals":[]}`)에서 아직 그 자리에서 끝나 뒤 킷을 재지 않는다(169 줄 근처). 종료 코드 2 는 맞고 계약이 이 경우까지 약속하지는 않았다.
  4. `run-evals.py` 에 대상 없는 바로가기를 킷 이름으로 직접 주면 인자 검사가 `is_file()` 이라 안내가 `evals/evals.json 없음` 으로 나온다(193 줄 근처). 종료 코드 2 는 맞다.
  5. `sync-evals.py` 의 `process_kit`(141 줄) 두 번째 읽기가 `UNREADABLE` 을 확인하지 않는다. 두 읽기 사이에 파일이 바뀌는 드문 경우에만 문제가 된다(위 두 번 읽기 항목과 같은 뿌리).
