# fs1 — 마지막 정리 (규칙 · 코드 · 시험)

- 계약: `.harness/sprint-contract-after-0929-final-sweep-rules.md` (28 조건, `conditions_digest: sha256:34a6430363f22fb0` · `measurement_digest: sha256:c360eda38254f32d`, 봉인 커밋 `1e003eb0`)
- 측정 파일 여섯: `.harness/.meta/after-0929-final-sweep-rules/` (커밋 `9f09098e`, 지문은 계약 배경 절과 같다)
- 기준 판 `cacd9da3`. QA 판정과 계약 `status: done` 은 하지 않았다.

## 항목별 결과

| 항목 | 결과 | 커밋 |
| --- | --- | --- |
| ex2 검토 1 | `search-strategy.md` 역방향 금지 문단을 「`.p8` 을 안내한다는 사실로부터 `.p8` 권장이나 `.p12` 의 deprecation 을」 로. 페이지 407 행 · 474 행(나쁜 예 목록)도 같은 뜻으로. `repo_p8_recommend=0` | `00942a26` · `4008518e` |
| ex2 검토 2 | `evals.json` 67 행을 「Firebase iOS 설정 문서는」 으로 좁힘 | `00942a26` |
| ex 남은 것 — 레포 전체 같은 주장 | `contract-schema.md` §측정 관례와 페이지 `#measure-habits` 에 한 줄 | `1e4da776` · `4008518e` |
| dz 검토 1 | `visuals.spec.js` 에 비교 시험 — 왼쪽에 f 를 고르면 이름표가 「시안 F」. 이름표를 빈 글자로 망가뜨린 사본에서 `failed=1` | `2512200f` |
| dz 검토 2 | 투표 카드 · 메모 칸을 `repeat(5, 1fr)` 에서 `grid-auto-flow: column` + `grid-auto-columns: minmax(0, 1fr)` 로. 768px 이하는 `grid-auto-flow: row` 로 되돌려 375 폭 배치는 그대로. 「한 줄」 시험 추가, BASE 틀 사본에서 `failed=1`. SKILL · 페이지 안내에 CSS 를 고치지 않는 이유를 적음 | `2512200f` · `4008518e` |
| dz 검토 3 | `design-mockup/SKILL.md` 참조 줄을 「개수 규칙 … 기준 원본」 으로 | `2512200f` |
| dz 검토 4 | §5.6 트레이드오프 문장을 「— 시안 밖 산출물의 4 개 이상도, 3 축 변주도」 로 (원본 md · 페이지) | `1e4da776` · `4008518e` |
| k1 남은 것 1 | `users.me.yaml` 에 비교 기준값 블록 (`state: pending`, 값은 스냅샷 manifest 에서). 모르는 값(`manifestDigest` · `rawDigest` · `redactionRegistry` · `expiresAt`)은 지어내지 않고 뺐다 | `8db9e0ad` |
| k1 남은 것 2 | 시험 파일에 `_wall_budget_short_share: "0.00"` — `[미검증]` 이 슬롯 1 한 줄만. 표 두 곳도 「1 줄 (슬롯 1)」 | `577fb53d` · `4008518e` |
| k1 남은 것 3 | 설치본을 지운 사본 대조를 §측정 관례 한 줄로 | `1e4da776` · `4008518e` |
| h1 검토 | `ci-local.sh` 가 작업 전체 `if` · `env` · `defaults` 와 워크플로 전체 `env` · `defaults` 가 걸린 단계를 `UNSUPPORTED` 로 알림. `jobs` 가 사전이 아니면 종료 코드 2. 시험 두 경우 추가 — 기준 판 도구로 돌리면 종료 코드 1 | `30dd1db7` |
| lt 남은 것 | 경로 목록 넘기기(`xargs` · 배열)를 §측정 관례 한 줄로 | `1e4da776` · `4008518e` |

## 자기 측정 (TIP `4008518e` 기준)

- `texts.sh` — 조건이 요구한 값 전부 (`ss_new=1` · `repo_p8_recommend=0` · `cs_l1..3=1` · `ch_l1..3=1` · `fx_key=0.00` 등). `sec_lines md=62 html=42`
- `grid-rows.js` — 여섯 줄이 스크립트-01 기대와 글자 그대로 같음, 종료 코드 0
- `api-baseline.py` — `block=1 state=pending nd=1 media=1 mode=1 lineage=1 extra=[] others=0`, 종료 코드 0
- `spec-neg.sh` — `none rc=0 passed=2 failed=0` · `label applied=1 rc=1 failed=1` · `oldgrid applied=2 rc=1 failed=1`
- `ci-scope.sh` — 네 경우 모두 스크립트-04 기대대로, `FAIL ` 줄 0
- `test-ci-local.sh` — `PASS` 6 · 종료 코드 0. 기준 판 도구로는 `FAIL` 4 줄 · 종료 코드 1
- 오류-01 — `none` · `jobs: []` · `name: x` 셋 모두 종료 코드 2, `steps=` 줄 0
- `bambu-nosl.sh` — `here 결과: 28 경우 중 불일치 0 rc=0` · `noslicer … 건너뜀 20 rc=0 left_paths=0` · `thin-unreadable fails=1 unv=1 wall=0 rc=1`. 음성 대조(시험 파일만 BASE) 는 `불일치 1` · 종료 코드 1
- 문서 페이지 다섯 — 공통 CSS 링크 각 1, `check-docs-a11y.js` `5/5 PASS`
- markdownlint-cli2 0.23.2 (MD013 끔) 다섯 md 경고 0 · `shellcheck` 두 파일 종료 코드 0 · `validate-plugin.py --check=code-fence` · `--check=frontmatter` 종료 코드 0
- 구조-01 병합 0 · BAD 0 · 커밋 9 (이 노트 커밋 전) · 구조-02 범위 밖 0 · 봉인 `SEAL_OK` · `MEASURE_OK`

## 로컬 CI

- `scripts/ci-local.sh` — `steps=44 run=39 skip=5 unsupported=0 failed=0`, 종료 코드 0. CI 에만 있는 단계(api-kit docs · drift 표 · 원인 표 사본 · measure helpers · bambu 시험 · Playwright 두 단계)도 모두 `PASS`
- 옛 도구 — 모든 줄 `rc=0`, SKIP 은 `feedback-agg-test SKIP (yq 없음)` 하나

## 킷 판 번호 판단 (올리지 않았다 — 합친 뒤 main 에서)

- onboarding-kit · harness · bambu-kit · design-kit: patch (문서 문장 · 시험 · 틀 CSS 고침, 동작 추가 없음)
- api-kit: 시험 예시 파일만 바뀌어 판 번호를 올릴 필요 없음
- `scripts/` 는 킷이 아니다

## 남은 것

- 「ex 남은 것 — 새 규칙 넷」(벽시계 문자열 모양 · PRD/ADR 경계 · 조회일/갱신일 분리 · 서비스 계정 선택 나무) — 새 규칙이라 사용자 확인 전에는 넣지 않았다. 보고 때 물어야 한다.
- api-kit 예시의 다른 네 계약에는 비교 기준값 블록이 없다 — 이번 항목은 보류 상태를 글로만 적은 `users.me` 하나였다 (범위 경계).
- 「k1」 이라는 검토 이름이 `after-kaizen-0928/k1-notes.md` 와 `remaining.md` 의 다른 회차 검토에 겹쳐 쓰였다. 출처를 되짚을 때 폴더까지 같이 적어야 한다 (교차 진단 지적, 계약 배경 절에 적음).
- QA 판정은 APPROVE (28/28, 리포트 `.harness/sprint-feedback-after-0929-final-sweep-rules.md`), 계약 `status: done`. 교차 진단은 부모 세션 몫(`cross_diagnosis_by: pending-parent`).
- 독립 검토 참고 1 (막지 않음, 범위 밖·이번 변경 전부터 있던 일) — `scripts/ci-local.sh` 가 작업 전체의 `strategy.matrix` · `continue-on-error` · `container` · `runs-on` 을 `UNSUPPORTED` 로 알리지 않고 그냥 돌린다. matrix 단계는 `${{ matrix.x }}: bad substitution` 으로 `FAIL`, `continue-on-error: true` 작업은 CI 와 달리 `failed=1` 로 센다. 지금 레포 CI 파일은 이 열쇠를 안 써서 결과에 영향이 없어 이번엔 두었다. 쓰기 시작하면 이번 `if` · `env` · `defaults` 처럼 `UNSUPPORTED` 로 알리게 넓혀야 한다.
- 독립 검토 참고 2 (막지 않음) — `jobs: {a: null}` 처럼 내용 없는 작업이 있으면 안내 문장 대신 파이썬 오류 전문이 찍힌다. 종료 코드는 BASE 와 같은 2 라 동작은 같고 보기만 나쁘다. 오류-01 안내 경로에 한 줄 더하면 된다.
- 킷 판 번호(onboarding-kit · harness · bambu-kit · design-kit patch)는 main 에 합친 뒤 올린다.
