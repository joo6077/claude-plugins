# orca3 — bambu 오르카 가지 역사 다시 쓰기 (3 회차) 기록

계약: `.harness/sprint-contract-after-0929-bambu-orca-rewrite.md` (28 조건, 봉인 `a92de5fb57acd564` · 측정 `ef4626741ef9b51a`).
가지 `chore/ak3-orca3`, 시작 `bfdfd5a3`(`chore/after-kaizen-0928` 끝). 남은 일 목록 항목 A14 · C9 의 「역사 다시 쓰기」 몫이다.

## 한 일

원래 가지 `feat/bambu-kit-orca-h2s-feedback` 의 커밋 둘(`e55e8b3` 구현 · `42209be` QA 기록)을 병합 커밋 없이,
맨 위 폴더마다 한 커밋 · 새 서명으로 다시 만들었다. 원래 가지와 2 회차 가지(`chore/ak3-orca`)는 읽기만 했다.

| 커밋 | 맨 위 폴더 | 원래 커밋 | 내용 |
| --- | --- | --- | --- |
| `0775c648` | `.harness` | `e55e8b3` | 원래 계약 · 개정 · 근거 파일 셋 (원래 판 그대로) |
| `221a9127` | `bambu-kit` | `e55e8b3` | 스킬 본문 · 참조 문서 다섯 · 실행기 · 시험 파일 넷 |
| `44d8a3cc` | `docs` | `e55e8b3` | 문서 여섯 쪽 |
| `4a068a33` | `.harness` | `42209be` | 원래 계약(done) · QA 리포트 (원래 판 그대로) |

## 경로마다 어느 판을 골랐나

기준 내용은 측정 도구 `ref3.sh` 가 낸다. 통합 가지가 `c25d16ec` 뒤에 그 경로를 안 바꿨으면 2 회차 끝 판 그대로,
바꿨으면 세 판 합치기(우리 = 통합 `bfdfd5a3` · 기준 = `c25d16ec` · 그쪽 = 2 회차 `a2e762c2`)다.

| 경로 | 고른 판 | 통합 가지 쪽 변경 | 충돌 · 손본 곳 |
| --- | --- | --- | --- |
| `bambu-kit/skills/bambu-print-profile/SKILL.md` | 세 판 합치기 | k1 `66e6c74b` · lt `1bec9490` · rec `680ba88b` 모두 살림 | 충돌 둘 다 lt 가 빈 줄만 고친 자리 — Phase 3.1 절 앞 빈 줄, 4.4 「생성 후 사용자에게 안내:」 뒤 빈 줄. 2 회차 쪽을 골랐고, 빠지는 글줄은 없다. 대신 4.4 목록 둘(뱀부 · 오르카) 앞에 빈 줄을 더해 마크다운 경고를 2 → 0 으로 맞췄다 |
| `bambu-kit/evals/run-gate-fixtures.sh` | 세 판 합치기 | `f1d45d1b` · rec `680ba88b` 살림 | 충돌 0. 2 회차가 더한 설치본 필요 목록의 `카메라 준비 블록 없음` 한 자리만 들어왔다 |
| `bambu-kit/skills/bambu-print-profile/references/` 다섯 | 2 회차 판 그대로 | 없음 | 없음 |
| `bambu-kit/evals/gate-fixtures/machine-orca-*.json` 넷 | 2 회차 판 그대로 | 없음 (새 파일) | 없음 |
| `docs/bambu-kit/bambu-fields-baseline.html` | 세 판 합치기 | d1 `5c48e6c6` 살림 | 충돌 0 |
| `docs/bambu-kit/failure-recipes.html` | 세 판 합치기 | d1 `5c48e6c6` 살림 | 충돌 0 |
| `docs/bambu-kit/bambu-print-profile.html` | 세 판 합치기 + 두 줄 고침 | `0bb7567a` · d1 `5c48e6c6` · `c56d7203` 살림 | 충돌 0. 시험 파일 수 칸 `23 · FAIL 20 · 미검증만 1 · PASS 2` → `28 · 23 · 1 · 4`, 실행 줄 설명 `24 개` → `28 개`. 통합 판부터 틀려 있었고(실제 24 · 21 · 1 · 2) 2 회차는 봉인 조건 때문에 못 고쳤다 |
| `docs/bambu-kit/seam-recipes.html` · `surface-recipes.html` | 2 회차 판 그대로 | 없음 | 없음 |
| `docs/bambu-kit/tolerance.html` | 통합 판 + 원본 새 내용 | d1 `5c48e6c6` 이 새로 만든 쪽 | 원본 `tolerance.md` §1.3 절을 새 절 04 로 넣고 뒤 절 번호를 하나씩 밀었다(11 → 12 절). §3.2 볼트 통과 구멍 아래에 「구멍이 옆으로 누워 있으면 아래 보정값이 걸리지 않는다」 한 줄을 넣었다 |

## 조건별 자기 측정 (2026-09-29, 커밋 뒤 · `bambu-kit/` · `docs/` 변경 0)

| 조건 | 값 |
| --- | --- |
| 스킬-01 | 열한 경로 모두 차이 0 |
| 스킬-02 | `orig_ok=25/25` · 종료 코드 0 |
| 스킬-03 | 28 · 23 · 1 · 4 |
| 스크립트-01 | `결과: 28 경우 중 불일치 0` · 0. 음성 대조(카메라 줄을 `pass` 로) `불일치 1` · 1 |
| 스크립트-02 | `결과: 28 경우 중 불일치 0 · 건너뜀 20` · 0. 음성 대조(목록에서 한 자리 뺌) `불일치 1 · 건너뜀 19` · 1 |
| 스크립트-03 | `makerworld-fetch-test.sh` 0 · `validate-plugin bambu-kit` `Exit: 0` |
| 오류-01 · 오류-02 | 1 · 1 |
| 구조-01 ~ 구조-03 | `anc … no` 둘 · `merges=0` · `MANY`/`NOSIG` 0 · `cite e55e8b36 folders=.harness,bambu-kit,docs subj=3` · `cite 42209beb folders=.harness subj=1` · `files=14/14 harness_same=3/3` · `files=2/2 harness_same=2/2` · 커밋 수는 이 기록 커밋까지 7 |
| 구조-04 | 원래 가지 `42209beb…` · 2 회차 가지 `a2e762c2…` 그대로 |
| 구조-05 | 네 파일 모두 원래 가지 끝 판과 같음 |
| 구조-06 · 구조-07 | 0 · 0 (범위 블록 17 줄) |
| 구조-08 | 넷 차이 0 · 인쇄 쪽 4 · 1 · 1 · 1 · 1 · 표 차이 0 · 표 28 행 |
| 구조-09 | 낱말 여덟 모두 1 이상 · 제목 · 목차 · 절 12 · 1.3 제목 1 · 목차 1 · 빠진 통합 줄 0 |
| 구조-10 | 여섯 쪽 스타일 링크 1 · `cells=36 bad=0` |
| 금지-02 | `ls-remote` 종료 코드 0 · 0 줄 (세 가지 모두 원격에 없음) |
| 금지-03 · 금지-04 · 재사용-01 · 재사용-02 · 진단-01 · 진단-03 | 0 · 0 · 0 · 4 · 0 · 0 |
| 진단-02 | markdownlint-cli2 v0.23.2 · 경고 0 · `Linting: 6 files` · `Summary: 0 issues in 0 files` |
| 진단-04 | 로컬 CI · CI 전용 단계 — 아래 「로컬 CI」 |

## 로컬 CI

| 무엇 | 결과 |
| --- | --- |
| `ci-local.sh` (TMPDIR = scratch `o3ci/a`) | `rc=0` 25 줄 + `feedback-agg-test SKIP (yq 없음)` 한 줄 |
| `ci-only.sh` — CI 파일에만 있는 15 단계 | `ci_only=15/15` · 종료 코드 0 |
| `ci-only.sh` 음성 대조 (카메라 줄을 `pass` 로 바꾼 SKILL.md 사본) | `rc=1 bash bambu-kit/evals/run-gate-fixtures.sh` · `ci_only=14/15` |
| 문서 짝 검사 `detect-docs-drift.py --since bfdfd5a3` | 원본 여섯과 짝 페이지 여섯이 함께 바뀜 — 원본만 바뀐 짝 0 |

## 한국어 조건 번호 우회

| 무엇 | 어떻게 |
| --- | --- |
| 조건 번호 · 봉인 | 조건 번호는 한국어(스킬-01 등)로 썼다. 레포의 조건 세기 · 봉인 도구와 qa-evaluator 조건 세기는 영어 약자 번호만 읽어 이 계약을 0 조건으로 센다. 그래서 조건 수와 봉인 두 값을 측정 도구 `ids.sh`(`count` · `func` · `digest` · `mdigest`)로 셌다. 평가자도 이 도구로 센다. 레포 도구를 고치는 일은 다른 묶음 몫이다 |

## 킷 버전 판단

bambu-kit 은 **minor** 가 맞다 — 완료 검사가 프린터(machine) 설정 파일을 새로 받고 실패 레시피 네 종이 들어온 기능 추가다.
이번 범위에서는 버전을 올리지 않았다(릴리스 범위 밖).

## 남은 것

| 항목 | 이유 |
| --- | --- |
| 카메라 실물 확인 — 사용자가 할 일 | 오르카로 새 `.gcode.3mf` 를 뽑아 툴헤드 카메라 초기화 알림이 사라졌는지 봐 주세요. 기계로 확인할 수 없다 |
| 가지 올리기 · PR (A14 · C9 의 올리기 몫) | 계약 범위 밖이다. 금지-02 가 오히려 셋 다 안 올렸음을 잰다. 사용자 결정 뒤 다른 묶음이 한다 |
| 원래 가지 · 2 회차 가지 정리 | 지우지 않았다(구조-04). 이 가지가 합쳐진 뒤 사용자가 지울지 정한다 |
| bambu-kit 릴리스 (minor) | 범위 밖 |
| QA 판정 — 끝남 | qa-evaluator APPROVE, 28/28 통과. 리포트 `.harness/sprint-feedback-after-0929-bambu-orca-rewrite.md` |
| 교차 진단 | QA 리포트의 `cross_diagnosis_by` 가 `pending-parent` 로 남아 있다. 이 마무리 단계 범위에 없어서 띄우지 않았다. 부모 세션이 띄우거나 `none` 과 사유로 내린다 |
| 마크다운 경고 검사(진단-02) 독립 재실행 | 독립 검토 쪽 맥에 `markdownlint-cli2` 가 없어 QA 가 잰 값만 있다. 막는 결함은 아니다 |
