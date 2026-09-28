# h2 결과 노트 — 병렬 세션 훅이 못 잡던 커밋 모양 (B10)

계약: `.harness/sprint-contract-after-0928-parallel-guard.md` (봉인 `conditions_digest: sha256:44b7000a48c52ae6`, 측정 줄 `sha256:05e740133d2ff998`, 봉인 커밋 `fff869c`). QA 판정은 아직 안 했다.

고친 파일은 레포 밖 `~/.claude/hooks/parallel-session-guard.sh` 하나다. 공용 도우미 `_lib-hook-payload.sh` 는 손대지 않았다(지문 `dff1e68e…` 그대로). 고친 뒤 설치본 사본을 `h2-after/parallel-session-guard.sh` 에 두었다(sha256 `ccf1ddeb…`). 고치기 전 사본과 견주면 더한 줄 102 · 뺀 줄 24 이다.

## 무엇을 바꿨나

- 따옴표 덮기 awk 를 넓혔다. 치환은 따옴표 밖이든 큰따옴표 안이든 `$( … )` 와 역따옴표 둘 다 깊이를 올린다. 바깥 사본에서는 계속 덮고, 치환 안 원문을 꺼내 같은 규칙으로 따로 한 줄씩 덧붙인다
- 명령 위치에 있는 `bash -c` · `sh -c` 의 따옴표 인자도 꺼내 덧붙인다. 큰따옴표 인자는 역슬래시 한 겹을 벗긴다
- 닫히지 않은 치환 · 인자 · `(` 는 bash 가 문법 오류로 아무것도 안 돌리므로 덧붙이지 않는다. 짝 없는 `(` 부터 끝까지는 덮는다
- 명령 위치 벗기기에 `(` · `{` · `then` · `do` · `else` · `time` · `command` 를 더했다. `git -c k=v` 는 `-C` 처럼 값째 지운다
- 대상 폴더 찾기에서 `(cd …` 를 보고, `cd` · `git -C` 값에 `$` 나 역따옴표가 있으면 경고도 알림도 없이 지나간다
- 긴 명령에서 느려지지 않게 덮은 글자를 짧은 조각에 모았다가 붙인다. 같은 20415 글자 명령에서 CPU 시간이 고치기 전과 같다(0.24~0.29 초 대 0.24~0.28 초)

## B10 모양별 결과

측정은 모두 고친 뒤 설치본 `~/.claude/hooks` 에 대고 `h2-tools/h2-cases.sh` 로 돌린 값이다. 기대 출력 `h2-expected.txt` 와 줄마다 같다.

| B10 모양 | 시험 줄 | 결과 |
| --- | --- | --- |
| 큰따옴표 안 역따옴표 | K01 | `pre=1 post=1` (고치기 전 `pre=0 post=0`) |
| 치환 안 커밋 | K02~K05 | 넷 다 `pre=1 post=1` |
| `git -c k=v commit` | K06 · K07 | 둘 다 `pre=1 post=1` |
| 서브셸 `( … )` | K08 · K09, 경로 한정 K18 | `pre=1 post=1`, K18 은 `pre=0 post=1` |
| `{ …; }` | K10 | `pre=1 post=1` |
| `then` · `time` · `command` (같은 종류 `do` · `else`) | K11~K13 · K16 · K17 | 다섯 다 `pre=1 post=1` |
| `bash -c` · `sh -c` | K14 · K15, 경로 한정 K19 | `pre=1 post=1`, K19 는 `pre=0 post=1` |
| 풀 수 없는 대상 폴더 | D01 `git -C "$W"` · D02 `cd "$X"` | 둘 다 `pre=0 post=0 r=0 r2=0` (고치기 전 `pre=6 post=1 r=1 r2=0`) |

글자일 뿐인 N01~N13 은 모두 `pre=0 post=0` 그대로다. 서브셸 안 `cd` 를 가리키는 D04 는 `pre=0 post=1 r=0 r2=1` 로 그쪽 저장소의 HEAD 를 보인다(고치기 전에는 세션 저장소).

## 조건별 자기 측정

| 조건 | 값 | 음성 · 양성 대조 |
| --- | --- | --- |
| SK-00 | 0 | |
| SC-01 | diff 0, K 줄 19, 정답 도구 `ran=1` 19 | 고치기 전 사본 38 |
| SC-02 | diff 0, N 줄 13, 정답 도구 `ran=0` 13 | 넓힌 사본 24 |
| SC-03 | diff 0 | 고치기 전 사본 2 |
| SC-04 | cx3 시험 diff 0 | |
| SC-05 | us 시험 diff 0, 표준오류 0 줄 | |
| SC-06 | 시드 11 · 22 · 33 모두 `cases=40 has_dq_subst=0 … diff=0` | |
| SC-07 | `chars=20415 warned=1`, max_ms 182 · 462 · 209 (부하 평균 25 인 기계) | |
| ER-01 | E 줄 6, us ER01 줄 6, `bash -n` 0 | |
| ER-02 | diff 0 | 고치기 전 사본 4 |
| AR-01 | 0 줄 | |
| AR-02 | 커밋마다 맨 위 폴더 1 · `sig=ok`, 병합 0 | |
| AR-03 | 백업 지문 두 값 일치, 백업 커밋 시각 1790559669 < 훅 수정 시각, 다른 13 개 지문 차이 0, 파일 15 개, 설정 등록 각 1 | |
| AR-05 | 여섯 지문 앞 16 자리가 계약 값과 같다 | |
| RE-01 | 셸 함수 1 개(백업도 1) — 새 셸 함수 없음. 새 판별은 awk 안 함수라 다른 훅이 가져다 쓸 수 없다 | |
| RE-02 | `strip_heredoc_bodies` 2 | |
| DG-01 · DG-03 | 0 | |
| DG-02 | shellcheck 0 줄 · 0 줄 | 시험 파일 2 줄 |

SC-07 은 이 기계 부하가 커서 벽시계 값이 흔들린다. 같은 때 고치기 전 사본도 290~588 로 흔들렸다. 그래서 CPU 시간을 따로 쟀다(위 절).

## 톤 대조 (tone-kit:tone-guide 5 단계, 훅에 더한 102 줄)

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 what 대신 why | 0 | 통과 — 더한 주석 10 줄은 모두 실측 사고나 bash 동작 이유 |
| C-07 해설 3 줄 초과 | 0 | 통과 — 기존 머리 주석에 줄을 보탰고 새 덩어리는 3 줄 이하 |
| C-12 계산 근거 주석 | 0 | 통과 |
| N-08 한 글자 이름 | 0 | 통과 — awk 의 `k` 를 `found` 로 고친 뒤 0 |
| N-09 무역할 파일명 | 0 | 통과 — 새 파일 없음 |
| S-03 · S-04 뜻 없는 추출 · 넘기기만 하는 함수 | 0 | 통과 — awk 함수 여덟은 각자 한 가지 판별 |
| F 구분선 | 0 | 통과 |
| H 좋은 주석 보존 | 지운 주석 0 | 통과 — 옛 실측 주석은 모두 남겼다 |
| K-02 번역투 (locale §8 G-1) | 0 | 통과 |
| K-10 종결형 (G-2) | 0 | 통과 |

## 로컬 CI

`ci-local.sh` 요약 26 줄 가운데 `rc=0` 25 줄, 나머지 한 줄은 `feedback-agg-test SKIP (yq 없음)`. CI 파일에만 있는 단계 여덟의 종료 코드:

| 명령 | 종료 코드 |
| --- | --- |
| `python3 scripts/check-api-kit-docs.py` | 0 |
| `python3 scripts/detect-docs-drift.py --check-table` | 0 |
| `python3 scripts/check-cause-table-copies.py` | 0 |
| `bash harness/evals/measure/measure-helpers-test.sh` | 0 |
| `bash bambu-kit/evals/run-gate-fixtures.sh` | 0 |
| `bash bambu-kit/evals/makerworld-fetch-test.sh` | 0 |
| `npx playwright test design-kit/evals/visuals.spec.js` | 0 |
| `npx playwright test api-kit/evals/` | 0 |

## 킷 버전 판단

올리지 않는다. 레포 안에서 `.harness/` 밖 파일을 하나도 안 고쳤다(AR-01 0 줄). 바뀐 것은 레포 밖 개인 훅이다.

## 남은 것

- 새 시험을 CI 에 올리지 못했다. 대상 훅이 `~/.claude/hooks` 에 있어 GitHub CI 기계에는 없다. 도구는 `h2-tools/` 에 두었다
- B10 밖 모양은 손대지 않았다(계약 범위 경계). 시험해 보니 `! git commit` · `case … ) git commit` · 함수 정의 `f() { git commit; }` 는 여전히 못 잡는다. `eval` · `xargs` · `nohup` 뒤 커밋, 상대 경로 `cd ..` · `git -C sub` 의 대상 풀기도 그대로다
- `bash -c "cd /x; git commit"` 처럼 인자 안에서 폴더를 옮기면 커밋은 잡지만 대상 폴더는 세션 폴더로 본다. 인자 안 `cd` 는 대상 찾기가 안 보기 때문이다
- 따옴표 밖 `git -C /절대경로` 는 커밋 자신의 것이 아니어도 대상으로 본다(고치기 전과 같음). `git -C /다른저장소 add x && git commit` 은 다른 저장소를 짚는다. 좁히면 SC-06 무작위 맞대기가 `diff=4 · 2` 로 바뀌어 봉인 조건과 부딪혀 그대로 두었다
- `cd "$(git rev-parse --show-toplevel)" && git commit` 은 조용하다. 값을 못 푸는 `cd` 라 D02 와 같은 원칙이다(고치기 전에는 세션 저장소로 경고했다)

## 독립 검토 뒤 고친 것 (2026-09-28)

독립 검토가 BLOCKING 둘과 작은 것 하나를 찾았다. 설치본을 다시 고쳤고 사본은 `h2-after2/parallel-session-guard.sh`(sha256 `4eae4004…`)다. 첫 번째 고친 판 `h2-after/` 는 음성 대조용으로 그대로 둔다.

- 괄호 치환 뒤 붙은 커밋: 명령 앞 변수 대입 벗기기가 값을 빈칸까지 먹어 `h=______;git` 의 `;git` 까지 삼켰다. 대입 값이 따옴표 밖 `;` · `&` · `|` 에서 끝나게 했다
- `${x:-(}`: `${ … }` 안 괄호를 짝 없는 괄호로 세지 않는다
- 대상 폴더: 명령 전체의 `cd` · `-C` 에 `$` 가 하나라도 있으면 끝내던 줄을 뺐다. 따옴표를 덮은 사본에서 커밋보다 앞의 마지막 `cd` 와 커밋 자신의 `-C` 만 보고, 그 값을 못 풀 때만 조용히 지나간다. 커밋 메시지 속 `cd $X` · `git -C $W` 는 이제 대상 찾기에 안 걸린다

새 시험 `h2-tools/h2-review-cases.sh` (기대 출력 `h2-review-expected.txt`, 18 줄): 검토가 짚은 C1~C4 · `x=$(echo "(")` · `${x:-(}` · A1~A5 와 대상 폴더 T1~T7.

| 대상 | 값 |
| --- | --- |
| 설치본 | 기대 출력과 차이 0 줄 |
| 음성 대조: 첫 번째 고친 판 `h2-after/` | 차이 32 줄 |
| 고치기 전 `h2-backup/` | 차이 10 줄 — T2 · T3 · T5 · T6 · T7 (고치기 전부터 대상 폴더를 잘못 짚던 모양) |

검토 도구(`rev-h2/probe.sh`)로 다시 잰 값: 검토가 준 입력 세 벌 31 줄에서 검토가 짚은 모양은 모두 고치기 전과 같게 `pre=1 post=1`. 고치기 전과 다른 줄은 셋이고 뜻한 것이다 — bash 문법 오류라 아무것도 안 도는 `arr=( a b ; git commit` · `echo \$(; git commit`(진짜 bash 로 확인), 값을 못 푸는 `cd "$(…)"` 가 커밋 앞에 있는 것. 대상 폴더를 따로 본 입력 12 줄(`cases4.tsv`)에서 고치기 전과 다른 여섯도 모두 뜻한 것이다 — 커밋 뒤 `cd` 를 안 봄, 커밋 앞 마지막 `cd` 가 `$` 라 조용함, `git -c a=b -C /x commit` · `then cd /x` · `cd "/x"` 의 대상을 이제 짚음, D01 모양.

계약 조건 다시 잰 값:

| 조건 | 값 |
| --- | --- |
| SC-01 | diff 0, K 줄 19, 정답 도구 `ran=1` 19 |
| SC-02 | diff 0, N 줄 13, 정답 도구 `ran=0` 13 |
| SC-03 · ER-02 | diff 0 · 0 |
| SC-04 | cx3 시험 diff 0 |
| SC-05 | us 시험 diff 0, 표준오류 0 줄 |
| SC-06 | 시드 11 · 22 · 33 모두 `cases=40 has_dq_subst=0 … diff=0` |
| SC-07 | `chars=20415 warned=1 max_ms=166` |
| ER-01 | E 줄 6, us ER01 줄 6, `bash -n` 0 |
| AR-03 (d) | 다른 13 개 지문 차이 0, 파일 15 개, `_lib-hook-payload.sh` 지문 `dff1e68e…` 그대로 |
| RE-01 · RE-02 | 셸 함수 1 개 · `strip_heredoc_bodies` 2 |
| DG-02 | shellcheck 0 줄 · 0 줄 |
| DG-05 | 요약 26 줄 중 `rc=0` 25 줄 + `feedback-agg-test SKIP (yq 없음)`, CI 파일에만 있는 단계 여덟 모두 0 |

톤 대조(이번에 더한 줄): C-01 0 · C-07 0 (새 주석 덩어리는 모두 3 줄 이하, 대상 폴더 머리 주석은 옛 줄을 바꿔 쓴 것) · N-08 0 (`next_word` · `resolve` · `word_from` · `expect_command` · `flag`) · S-03 · S-04 0 · F 0 · H 지운 실측 주석 0 (「마지막에 나온 것이 이긴다」 한 문장만 규칙이 바뀌어 고쳐 썼다) · locale G-1 · G-2 0.
