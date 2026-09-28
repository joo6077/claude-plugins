# dz — 시안 개수 규칙 (위 제한 없이 최소 5 개부터)

- 계약: `.harness/sprint-contract-after-0928-mockup-count.md` (20 조건, 봉인 `conditions_digest: sha256:c70a4f0bd6616598` · `measurement_digest: sha256:15e178ac7f1ba94d`)
- 가지: `chore/ak3-dz`, 기준 커밋 `c25d16e`
- 남은 일 목록 항목: A4 · C3 (KD-4 design:P2 규칙 방향)

## 교차 진단 반영 (봉인 전)

SK-03 이 §5.6 예시 표를 5 행으로 늘리라고 하면서 같은 절의 「상한 3」 은 그대로 두어, 측정이 통과해도 문서가
스스로 부딪힐 수 있다는 지적이었다. 예시는 실제로 시안(`mock/a*.html`) 예시라서 5 행으로 늘리되, 표 바로 위에
「이 예시는 시안 규칙(최소 5)이고 시안이 아닌 탐색형 산출물은 상한 3」 이라는 이름표 줄을 두고 Good 줄에도
「시안」 을 적게 했다. `rows.sh` 에 `label` 검사를 더하고 `good5` 에 「시안」 을 넣었으며, SK-03 · AR-02 문구에
반영한 뒤 봉인했다. 조건을 좁히는 방향이다. 알려진 답 세 가지(이름표 없는 사본 → `label=0`, 이름표 넣은 사본 → `label=1`,
HTML 파일 없는 사본 → `MISSING_FILE` · 종료 코드 2)를 봉인 전에 돌려 확인했다.

## 커밋

| 커밋 | 폴더 | 내용 |
| --- | --- | --- |
| `a6cf695` | `.harness` | 계약 봉인 (파일 1 개) |
| `89ecc67` | `.harness` | 측정 파일 7 개 |
| `b3085f7` | `design-kit` | 스킬 · 참조 · 평가 사례 · README · 틀 · 여섯 시안 시험 |
| `b573a49` | `harness` | §5.6 조항 1 분리 · 예시 5 행 · 요약 표 |
| `c3a36c3` | `docs` | 문서 쪽 다섯 |

## 항목별 결과 (TIP 사본에서 직접 잰 값)

| 조건 | 값 |
| --- | --- |
| SK-01 | S01~S04 모두 `ok=1` |
| SK-02 | S05~S08 모두 `ok=1`, sync-docs 「모든 README가 동기화 상태입니다.」 |
| SK-03 | S10 · S11 `ok=1`, `md_rows=5 md_good5=1 md_label=1` |
| SK-04 | (a) 0 (b) 0 (c) 5 (d) 5 (e) 1 |
| SC-01 | `-g 'templates/mockup.html 시안 6 개'` 4 passed · rc=0, 스펙 안 `templates/mockup.html` 3 번 |
| SC-02 | 옛 틀로 덮은 사본(SK-04 (a) 4) → rc=1 · 2 failed(화살표 · 메모) · 2 passed |
| SC-03 | CI 줄 1, 전체 `visuals.spec.js` 160 passed · rc=0 |
| SC-04 | `ci-local.sh` rc=0 25 개(feedback-agg-test SKIP), CI 파일에만 있는 여섯 단계 rc=0, `Total: 14 plugins, 14 OK`, 전체 `npx playwright test` 168 passed |
| ER-01 | `KEEP_TOTAL n=21 ok=21 missing=0`, flutter-toolkit · react-kit 구간 차이 0 |
| AR-01 | S12~S19 `ok=1`, 쪽 검사 `PAGES checked=12 over=0 errors=0 css_bad=0` |
| AR-02 | S20 · S21 `ok=1`, `html_rows=5 html_good5=1 html_label=1`, 쪽 검사 `PAGES checked=3 over=0 errors=0 css_bad=0` |
| AR-03 | 범위 밖 경로 0, 커밋 다섯 모두 맨 위 폴더 1 개, design-kit · harness · docs 각 1 커밋 |
| AP-03 · AP-04 | design-kit `code-fence,frontmatter` · harness `code-fence` 모두 「1 plugins, 1 OK」 |
| RE-01 · RE-02 | 새 파일 0, `Object.keys(MOCKUP_CONFIG.variants)` 5 곳 |
| DG-01 · DG-03 | `scripts/release.sh` 변경 0 |
| DG-02 | markdownlint 0 · 0 · 2 · 0 · 0 (봉인 전 값과 같다), evals.json 읽기 rc=0 |
| DG-04 | SC-01 네 시험 모두 pageerror 0 확인, 쪽 검사 errors=0 |

측정 파일 sha256 앞 16 자리는 계약 공통 정의의 값과 모두 같다.

## 평가자가 알아야 할 것

- `sites.py` 의 S11 · S21 은 시작 정규식의 **첫 일치 줄**을 잰다. 두 파일 모두 첫 일치가 요약 표가 아니라 §5.6 안
  「이름 구분」 표의 Variant Budget 행이었다(봉인 전 값 `need_miss=최소 5|위 제한 없 old=0` 도 그 줄의 값이다).
  조건 문구의 뜻(요약 표 행)과 측정이 가리키는 줄이 달라, 두 줄을 모두 고쳤다 — 요약 표 행에 새 규칙을 넣고,
  이름 구분 표 행에는 「개수 상한」 을 남긴 채 「(시안은 최소 5 · 위 제한 없음)」 을 덧붙였다. 계약 범위 경계의
  「`:766` 이름 구분 표의 「개수 상한」 은 그대로 둔다」 는 지켰다(낱말은 그대로 있다). 측정과 조건 문구는 바꾸지 않았다.
- 틀에서 `TAB_COLORS` · `TAB_LABELS` 두 고정 목록도 지웠다. 비교 뷰가 여섯째 시안의 색과 이름을 못 찾기 때문이다.
  대신 `MOCKUP_CONFIG.variants[id].color` 와 `T[currentLang].tab[id]` 를 읽는다. 칸 묶음 목록(탭 · 패널 · 비교 선택 두 곳 ·
  투표 카드 · 메모 칸 · `MOCKUP_CONFIG` · 두 언어 tab 글자)은 계약 범위 경계에 적힌 것과 같다.

## 킷 판 번호 판단

- design-kit: minor — 스킬이 내는 시안 수가 바뀌고 틀이 여섯째 시안을 받게 됐다(동작 변경).
- harness: patch — 가이드 문서만 바뀌었다.
- 계약대로 이 묶음에서는 판 번호를 올리지 않는다. 묶음을 합친 뒤 릴리스에서 올린다.

## 남은 것

- QA 판정(qa-evaluator) — 이 작업자는 판정과 `status: done` 을 하지 않는다(지시).
- 판 번호 올리기 · 릴리스 · changelog — 계약 「하지 않는 것」. 묶음 병합 뒤 따로.
- `sites.py` 의 첫 일치 문제 — 한 줄만 재는 자리는 시작 정규식이 여러 번 맞으면 멈추게 고치는 것이 맞다.
  봉인된 측정 파일이라 이번에는 고치지 않았고 피드백 개선 제안에 남겼다.
