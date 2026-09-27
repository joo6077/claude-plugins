# cx3 결과 — 합친 뒤 어긋남 넷

계약: `.harness/sprint-contract-after-0926-merge-drift-fixes.md` (25 조건, 봉인 커밋 5e963dd).
봉인: `conditions_digest: sha256:6c4191696be56f14` · `measurement_digest: sha256:eac93e473d1b60da` · `locked_at: "2026-09-27 19:31"`.
봉인 직후 확인은 `SEAL_OK` · `MEASURE_OK` · `OK seal_commit files=1`. 교차 진단은 지적 0 건이라 조건을 고치지 않았다.

## 항목별 결과

### (1) design-mockup 단계 번호 — a7f66c0 (design-kit)

`SKILL.md:171` 과 `design-mockup.html:665` 의 「Step 2 가 폐기 칸의 경로를 따라」 를 「Step 0 이 …」 로 고쳤다.

- SK-01: `refs=8 ok=8 bad=0 unclassified=0`, 종료 코드 0 (고치기 전 `ok=6 bad=2`)
- SK-02: 옛 문장이 든 파일 0 개, 「폐기 칸의 경로를 따라 원문을 읽는다」 는 두 파일에 1 · 1

### (2) 종료 코드 표 인용 — f87e8f4 (scripts)

`scripts/check-api-kit-docs.py` 머리 설명 12 줄에 「exit 0 = 전부 통과, 1 = 소스→HTML 누락이 하나라도 있다. 종료 코드 의미: harness/evals/gate-exit-codes.md」 를 더했다. `check-docs-a11y.js` 와 같은 꼴이다.

- SC-05: `cite=12 rows=12 missing=0 extra=0`
- SC-06: 머리 20 줄에 `gate-exit-codes.md` 1 번. 표준출력 지문 `46d7e0adf3e6fed0…`, 종료 코드 0, `--json` 지문 `28297b8c9f8b5da2…` 로 고치기 전과 같다. `py_compile` 0

### (3) 병렬 세션 훅 따옴표 — 레포 밖 `~/.claude/hooks/parallel-session-guard.sh`

고치기 전 두 파일을 `cx3-backup/` 에 담아 44bb72c 로 먼저 커밋했다(커밋 시각 1790505115, 훅 수정 시각 1790505686).
따옴표 덮기 awk 가 큰따옴표 안 `$(` 를 만나면 치환 깊이를 하나 올리고, 그 깊이의 따옴표 상태와 괄호 수를 따로 센다. 짝 맞는 `)` 에서 바깥 큰따옴표로 돌아간다. `$((` 는 산술이라 올리지 않는다. 치환 안 글자는 모두 `_` 로 덮는다. `_lib-hook-payload.sh` 는 고치지 않았다(지문 `dff1e68e…` 그대로). 새 셸 함수는 없다.

- SC-02: `guard-expected.txt` 와 차이 0 줄 (X1~X5 `pre=1 post=1`, T1~T3 `pre=0 post=0`, E1 두 줄 `rc=0 out=0 err=0`)
- SC-03: us 묶음 시험 차이 0 줄, 표준오류 0 줄
- SC-04: 시드 11 · 22 · 33 모두 `cases=40 has_dq_subst=0 diff=0` (`warned=1 · 4 · 1`)
- ER-01: `ER01-` 여섯 줄 모두 `rc=0 empty=1 stderr_empty=1`, E1 두 줄, `bash -n` 0
- AR-03: 백업 지문 `5bf30dd5…`, 나머지 13 개 지문 대조 실패 0, 파일 수 15
- RE-01 새 함수 수 1 (백업도 1, `emit` 하나) · RE-02 `strip_heredoc_bodies` 2 번
- 덤으로 잰 것: `"$( (cd a; ls) )"; git commit` 과 치환 안 주석 속 `'` 뒤 커밋도 잡는다

### (4) superseded 상태 — 2a29cdf (harness) · b531389 (.harness)

스키마 `### v5 신규 필드` 표의 `status` 값에 `superseded` 를 넣고 `superseded_by` 행(새 판 슬러그, 필수, 사슬 금지, 봉인 그대로)을 더했다. `### status 해석 규칙` 에 superseded 를 active 후보와 레거시 양쪽에서 빼는 줄, 메타데이터 예시 `status:` 주석에 `superseded` 를 넣었다. 계약 고르기 두 곳을 한 줄씩 고쳤다 — qa-evaluator 1-c `elif [ "$st" = "done" ] || [ "$st" = "superseded" ]`, 스키마 ladder `"done"|superseded) ;;`. 상태 표 넷과 페이지 판(`contract-schema.html` 의 예시 · 필드 표 · 해석 목록 · ladder 코드)도 맞췄다. 옛 계약 셋은 앞머리에 `superseded_by:` 한 줄씩만 더했다.

- SC-01: `ladder-expected.txt` 와 차이 0 줄, 종료 코드 0
- SK-03: (a) `status` 행 `superseded` 2 번 (b) `superseded_by` 행 1 개 (c) 해석 규칙 절 1 (d) 예시 줄 1
- SK-04: 1 · 1 · 1 · 1 · 1
- ER-02: `superseded=3 valid=3`, 셋 다 `seal=OK`, 기준 커밋 대비 차이는 `+superseded_by:` 세 줄

## 공통 측정

- DG-02: 마크다운 경고 0 · 0 · 8 · 0 · 0 (contract-schema.md 는 고치기 전과 같은 8), `shellcheck` 0 줄, `py_compile` 0
- AP-03 · AP-04: `validate-plugin.py --check=code-fence` · `--check=frontmatter` 모두 Exit 0
- 그 밖 검사: `validate-plugin.py` 14 킷 OK · `sync-docs --check-only` 0 · `sync-evals --check-only` 0 · `check-reviewer-protocol-copies` 0 · `check-cause-table-copies` 0 · `detect-docs-drift --check-table` 0 (어긋남 0)
- 로컬 CI 요약: `rc=0` 25 줄, `feedback-agg-test SKIP (yq 없음)` 1 줄, 그 밖 0 줄 — 봉인 전 기준과 같다

## tone-kit:tone-guide 5 단계 대조

대상은 이번에 더한 줄 34 줄(레포 안 추가 줄 · 훅 추가 줄 · 옛 계약 셋 추가 줄).

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 · §8 G-1 번역투 6 종 | 0 | 통과 |
| K-04 · G-2 `합니다`체 | 0 | 통과 |
| K-10 · §9 자기모순 검사 | 0 | 통과 |
| C-01 why 만 남기기 (훅 주석 3 줄) | 0 | 통과 — 실측한 실패 모양과 `$((` 를 빼는 이유만 적었다 |
| C-04 구분선 · 마커 | 0 | 통과 |
| C-07 해설 3 줄 초과 | 0 | 통과 — 새 주석은 3 줄 |
| C-13 자화자찬 | 0 | 통과 |
| N-08 한 글자 이름 | 0 | 통과 — 처음 쓴 `d` · `q` · `p` 를 `depth` · `quote_at` · `paren_at` 으로 고쳤다 |
| S-04 · S-06 넘기기만 하는 래퍼 · 헬퍼 사슬 | 0 | 통과 — 새 함수 없음 |
| K-11 새로 붙인 이름 | 0 | 통과 |

## 킷 버전 판단

- design-kit: 문서 문장 두 곳 — patch 감
- harness: 계약 형식에 허용 값 하나와 칸 하나가 늘고 평가자 계약 고르기가 바뀐다 — 뒤로 호환되는 추가라 minor 감
- scripts · 훅: 킷이 아니라 버전 없음

버전 올리기 · 릴리스 · 푸시는 하지 않았다(계약 범위 밖).

## 남은 것

- QA 판정: APPROVE (25 조건, N/A 3 은 사유 참 확인). 계약 `status: done` 과 QA 리포트는 커밋 fb5374b
- 교차 진단 `cross_diagnosis_by: pending-parent` — 부모 세션이 이어받아야 한다. 전역 피드백은 `~/.harness/feedback/evaluator/1a3bcba6-2026-09-27T195402-bda55d45-12096.yaml`
- qa-evaluator Step 1-e 봉인 대조의 `status: (active|done)` 거르기는 그대로 둔다(범위 경계). superseded 계약은 평가 대상이 아니라서다
- 훅이 원래 못 잡는 모양(`git -c k=v commit` · 서브셸 · `bash -c` · 치환 안에서 도는 진짜 커밋 등)은 그대로다
- AR-02 재는 명령(`git log --format=%B | tail -2`)이 틀렸다. `%B` 끝에 붙는 빈 줄 탓에 줄 순서가 뒤집혀 여덟 커밋 모두 헛 FAIL 이 난다. 끝 빈 줄을 지우고 재면 여덟 모두 통과. 다음 계약에서 이 모양을 쓰지 마라
- 독립 검토(막는 결함 0)에서 나온 약점. 모두 이번 변경 전부터 있었거나 범위 밖이다
  - 훅: 큰따옴표 안 역따옴표 치환(`` echo "`echo "it's"`"; git commit -m x ``)은 고친 판 · 백업 판 모두 경고 0. `$(` 만 고쳤고 역따옴표는 같은 방식으로 다루지 않는다
  - 훅: 치환 안에서 도는 진짜 커밋(`x=$(git commit -m y)` · `echo "$(git commit -m y)"`)은 두 판 모두 0
  - 계약 고르기: `status: superseded   # 새 판 있음` 처럼 줄 끝 주석이 붙으면 `fm_get` 이 주석까지 값으로 읽어 옛 계약을 도로 채점한다(`qa-evaluator.md` · `contract-schema.md` 3.5b 둘 다). `done` · `active` 에도 같은 한계다. 따옴표로 감싼 값은 제대로 빠진다
  - `superseded` 계약만 있는 폴더는 `4 BLOCKED` 로 끝난다(`0 계약부재` 아님). `done` 만 있을 때와 같고 기대 출력에도 그렇게 적혀 있다
  - `superseded_by` 가 가리킨 계약이 실제로 있는지, 그것도 `superseded` 는 아닌지 기계로 확인하는 곳이 없다. 문서 규칙뿐이다. 이번 셋은 `-r2` 파일이 있고 셋 다 `status: done` 임을 손으로 확인했다
  - `harness/skills/sprint-contract/SKILL.md` 에 `superseded` 로 바꾸는 법이 없다. 같은 슬러그 기존 계약을 다루는 분기(약 320–329 줄)에도 없다. 형식은 `contract-schema.md` 에만 있다
  - 참고: `qa-pending-check.sh` · `commit-guard.sh` 는 `active` 만 보므로 `superseded` 를 따로 고칠 필요 없다. `step-refs.py` 는 `refs=8 ok=8 bad=0 unclassified=0`
- 버전 올리기 · 릴리스 · 푸시 · 통합 폴더 합치기는 하지 않았다
