# fin 묶음 기록 — 평가 실행기 남은 다섯 · 레포 밖 훅 둘을 레포로

- 계약: `.harness/sprint-contract-after-0930-final.md` (28 조건, 봉인 `conditions_digest` `26b3fa100e0df3b3` · `measurement_digest` `51181469f470782b`)
- 가지 `chore/ak3-fin`, 시작 판 `7fe274fc`(가지 `chore/ak3-ev` 끝). push · 합치기 · QA 판정은 하지 않았다.

## 항목별 결과

| 항목 | 결과 | 커밋 |
| --- | --- | --- |
| 봉인 | 교차 진단 지적 하나(스크립트-11 이 run 줄 개수만 봐서 지우고 끼워도 통과)를 반영했다. 새 넷을 뺀 run 목록이 시작 판과 차례까지 같아야 하도록 좁히고, 두 줄 자리를 맞바꾼 사본으로 `kept=0` · 1 을 음성 대조로 적었다. 6.5 재통과 뒤 봉인, 봉인 커밋 파일 1 개 | `7e4e725d` |
| 측정 도우미 | 지문 `f066b5cdac40442c` 그대로 커밋 | `efbb6cd6` |
| (1) · (2) 객체가 아닌 내용 | 두 실행기가 내용이 객체가 아니면 경로와 `내용이 객체가 아니다 (null)` 같은 한 줄을 찍고 못 읽은 킷으로 센다. 나머지 킷을 끝까지 재고 2 | `4041db99` |
| (3) 항목 0 개 | `run-evals.py` 가 그 자리에서 멈추지 않고 끝까지 잰 뒤 `항목 없는 킷 N 개: …` 를 찍고 2. 못 읽은 킷 줄이 먼저다 | `4041db99` |
| (4) 이름 준 대상 없는 바로가기 | 인자 검사를 `os.path.lexists` 로 바꿔 `UNREADABLE <경로> (바로가기 대상 없음)` 으로 잰다. 자리가 없는 킷 안내는 그대로 | `4041db99` |
| (5) 두 번째 읽기 | `sync-evals.py` 의 `process_kit` 이 못 읽음 표시를 받으면 추적 출력 대신 못 읽은 킷으로 센다. 두 읽기는 합치지 않았다 | `4041db99` |
| 시험 | run 시험 경우 10 ~ 20, sync 시험 경우 7 ~ 15. 시작 판 도구로는 run `10,11,12,13,14,17,18,19` · sync `7,8,9,10,11,14,15`, 지나친 판으로는 run `3,9,15,16,17,18` · sync `2,6,12,13,14` 만 실패 | `4041db99` |
| 훅 둘을 레포로 | `lint-contract-oracle.sh` · `qa-pending-check.sh` 와 두 훅이 부르는 `_lib-hook-payload.sh` 를 `~/.claude/hooks/` 에서 바이트 그대로 `harness/evals/hooks/` 로 옮겼다. `hooks.json` 등록은 하지 않았다. 훅 시험 둘은 기본값이 레포 본이고 `CLAUDE_HOOK_LIB` 를 훅에 넘긴다 | `1ac91eda` |
| 맞대기 검사 | `scripts/check-user-hook-copies.py`(설치본이 없으면 `설치본 없음 — 건너뜀` · 0, 다르면 `다름:` 줄 · 1)와 그 시험 6 경우 | `4041db99` |
| CI | 훅 시험 둘 · 맞대기 시험 · 맞대기 검사 네 단계를 더하기만 했다. 평가 시험 이름은 「스무 경우」 · 「열다섯 경우」 | `75437b96` |
| 리눅스 | 도커 `ubuntu:24.04`(mawk · GNU grep)에서 훅 시험 둘과 맞대기 시험이 모두 0. 리눅스 수정은 없어서 설치본에 옮길 줄도 없다 | — |

## 자기 측정 (W, TMPDIR 은 scratch 아래, `npm ci` 뒤)

- 스크립트-01 `cases=15 right=15 ok=1` · 스크립트-01-base `cases=15 base_right=0 base_all_wrong=1` · 스크립트-02 `cases=9 right=9 ok=1 mut_right=0 mut_ok=1` · 스크립트-03 `cases=4 right=4 ok=1` · 스크립트-04 `cases=4 right=4 ok=1` · 스크립트-05 `cases=2 right=2 ok=1`
- 스크립트-06 `run_ok=1 sync_ok=1 run_base_ok=1 sync_base_ok=1 run_mut_ok=1 sync_mut_ok=1 ci_ok=1`
- 스크립트-07 `runs=4 pass=4 ok=1 stub_rcs=1,1 stub_ok=1 noexport_rcs=1,1 noexport_ok=1 base_rcs=2,2 base_ok=1` · 스크립트-08 `results=3 mawk=1 gnu_grep=1 ok=1`
- 스크립트-09 `none_ok=1 same_ok=1 flip_ok=1 installed_ok=1` · 스크립트-10 `tail=[경우 6 개 중 통과 6] ok=1 stub_fails=4,5,6 stub_ok=1` · 스크립트-11 `base_runs=52 runs=56 new_once=1 kept=1 added_only=1`
- 오류-01 `cases=6 right=6 ok=1 absent_same=1` · 오류-02 `lines=7 same=1` · 구조-02 `miss=[] stale=[] ok=1` · 구조-04 `files=5 same_set=1 registered=[] not_registered=1` · 구조-05 `files=3 ok=1` · 재사용-02 `added=2 ok=1`
- `.py` 여섯 `py_compile` 0, `.sh` 다섯 `bash -n` 0 · `shellcheck` 0 줄, `validate-plugin.py --check=code-fence` 0
- 로컬 CI(`scripts/ci-local.sh`) `steps=56 run=51 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0. CI 파일에만 있는 단계와 새 시험 열둘 모두 종료 코드 0 (`npx playwright test` 174 passed)

## tone-guide

- 1 단계: 오버레이 `.claude/tone-project.md`(어댑터 없음 · 주석 한국어)와 코어 네 파일의 규칙 표를 레포 판으로 읽었다. 걸리는 규칙은 C-01 · C-07 · C-15 · H(보존) · N-08 · N-09 · S-04 · S-07 · J.
- 5 단계: 더한 줄에서 구분선 · 템플릿 표시 · fallback 이름 · 새 한 글자 이름 · 무역할 파일 이름 0 건. `enumerate` 의 `i` 는 옛 줄을 고친 자리라 그대로 두었다. 새 주석은 모두 까닭을 적은 줄이고, 옛 까닭 주석은 지우지 않았다. 옮긴 세 파일은 설치본 바이트 그대로라 손대지 않았다.

## 킷 버전 판단

harness 판 번호는 올리지 않는다. 바뀐 harness 파일은 시험 폴더 `harness/evals/hooks/` 뿐이라 설치되는 스킬 · 에이전트 · 훅 동작이 바뀌지 않는다. `scripts/` · `.github/` 는 킷 밖이다.

## 남긴 것

- QA 판정과 `status: done` — 이 묶음에서 하지 않는다(부모 지시).
- 앞 묶음 측정 가운데 ev 계약 `스크립트-04` 와 end 계약 `스크립트-06` 은 시험 경우 수가 늘어 이제 1 을 낸다. 경우를 더한 결과라 일부러 바뀐 값이고, 그 계약들은 이미 `done` 이라 다시 재지 않는다.
- 설치본과 레포 본이 갈리면 맞대기 검사가 로컬 CI 에서 1 로 알린다. 어느 쪽을 고칠지는 그때 사람이 정한다.
