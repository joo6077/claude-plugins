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
- QA 판정 · `status: done` 전환 · push · PR 은 이 묶음 밖이다.
