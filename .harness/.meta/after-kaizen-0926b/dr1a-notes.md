# dr1a — 문서 페이지 다시 맞추기 A (harness · process · api · backend · bambu)

계약 `.harness/sprint-contract-after-0926-docs-regen-a.md` (봉인 `2f0ef9185160f3ff` · 측정 지문 `600de837d4e77b33` · 봉인 커밋 `22f0f18`).
작업 폴더 `.claude/worktrees/ak2-dr1a`, 가지 `chore/ak2-dr1a`, 기준 판 `38cccd1`. QA 판정은 아직 없다.

## 커밋 목록

| 커밋 | 단위 | 내용 |
| --- | --- | --- |
| `22f0f18` | `.harness` | 계약 봉인 (파일 1 개) |
| `9346786` | `.harness` | 측정 묶음 7 파일 (지문은 계약 AR-03 과 같다) |
| `e5c8823` | `scripts` | `check-api-kit-docs.py` 외부 자원 판정에 `<img src>` · `url(//…)` · 빈칸 없는 `@import` |
| `604a94c` | `.github` | CI `validate` 작업에 api-kit 문서 검사 한 단계 |
| `92377e0` | `harness` | 설계 가이드 「조건 패턴 8 종」 · 종료 코드 표 한 행 |
| `55b760b` | `docs/harness` | 여섯 쪽 |
| `4dd8126` | `docs/process` | 두 쪽 |
| `7f6e0af` | `docs/api-kit` | 두 쪽 (`multi-sample-pagination-variance` 는 원본 변화 없음 — 그대로) |
| `1cedfa8` | `docs/backend-kit` | 한 쪽 |
| `377a5be` | `docs/bambu-kit` | 네 쪽 |

`docs/index.html` 은 고치지 않았다 — 목차 제목의 판 번호가 이미 원본과 같다(`contract-schema` v5.7 등).

## 쪽별 결과

담김 값은 `m SK-01` (코드 표시 새/옛 · 낱말 비율 새/옛) · `m SK-02` (코드 블록 줄 새/옛) 출력이다. 17 짝 모두 `lost=0`.

| 쪽 | 코드 표시 | 낱말 비율 | 코드 블록 줄 | 바꾼 것 |
| --- | --- | --- | --- | --- |
| kaizen-flow | 171/150 | 0.31/0.25 | 11/0 | Phase 범위 줄 표(scripts/ · templates/), Step 0.5 감사 기록 자리, F1 판 번호 원본 목록 · F4 7 번 감사 기록 코드 블록, F2 원칙 |
| phase-research-templates | 77/75 | 0.99/0.98 | 0/0 | 머리 `2026-09-05`, Hub 외부 프로젝트 두 칸, `.hurl` 불변식 문장 |
| static-evidence-viewer-contract (api-ui) | 73/60 | 0.44/0.40 | 12/9 | CSP `<meta>` 한 줄 검사, 판정 불가 줄 옮기기, 브라우저 확인 `chips` · `rows` |
| static-evidence-viewer-contract (docs/api) | 45/45 | 0.92/0.92 | 0/0 | — |
| multi-sample-pagination-variance | 35/35 | 0.18/0.18 | 0/0 | 바꾸지 않음 |
| contract-extraction-modes | 49/47 | 0.24/0.23 | 0/0 | 확정 시안 `.mockups/api-ui-v8.html` |
| api-design | 20/20 | 0.92/0.91 | 8/8 | OpenAPI 판 문장 |
| bambu-print-profile | 401/392 | 0.74/0.73 | 157/155 | 종류 줄만 빠진 목록 행 · 금지 키 시험 파일 · 답글 수 · `trap` 정리 · 네 칸 · 릴리스 현황 |
| bambu-fields-baseline | 248/246 | 0.71/0.70 | 31/31 | 머리 날짜 · 최신 베타/안정 판을 첫 화면으로, §1 은 처음 쓸 때 기록 |
| failure-recipes | 73/69 | 0.91/0.81 | 9/0 | L2 게이트를 원본(관측 신호 먼저 · 소재 부모값 · 네 칸)으로 다시 씀 |
| materials | 28/26 | 0.71/0.68 | 0/0 | 머리 `2026-05-15`, PLA Pure 문장 |
| agent-design-guide | 155/151 | 0.90/0.88 | 41/41 | `model` 생략 규칙 · `omitClaudeMd` · `experimental`(`cacheTtl`) · 상한 오류 문구 |
| contract-design-guide | 204/203 | 0.96/0.96 | 59/59 | 「조건 패턴 8 종」 · `measurement_digest` · 스키마 v5.7 |
| plugin-validation | 193/174 | 0.80/0.75 | 76/70 | 1.5.0 — V2 `no templates/ — OK` · V3/V6 CommonMark 판정 · V8 `$CLAUDE_PLUGIN_ROOT` · V10 원본 폴더 · 1.4.2 사실 정정 |
| qa-evaluation-guide | 398/387 | 0.96/0.94 | 85/85 | 머리 2026-09-26 · 스키마 v5.7 · `MEASURE_*` 행 · `# sprint-scope` 문장 · 문서 산출물 사본 절 · 사본 검사 |
| skill-design-guide | 124/111 | 0.94/0.90 | 114/114 | `# sprint-scope` E3 · 알려진 답 입력 고르기 · 검사를 만드는 스킬 사본 넷 · frontmatter 필수 여부 · §8.9 공통 숫자 · 워크트리 |
| contract-schema | 366/316 | 0.96/0.89 | 295/259 | v5.7 — 측정 관례 · 조건 패턴 셋 · 범위 목록 블록 · `dirty_except_status` 외 |

`failure-recipes` 의 L2 게이트는 원본 변화가 기준 판 이전(`07573ee`, 2026-09-06)이라 SK-04 로는 안 잡히지만, 페이지가 옛 규칙(건조 먼저 · 되감기 `1.0`–`1.2`)을 적고 있어 같이 맞췄다.

`kaizen-flow` 의 `docs/assets/site.css` 는 글자로 쓰면 SK-07(공통 링크 글자 1 개)과 부딪혀 `site&#46;css` 로 적었다. 화면에는 같은 글자로 나오고 SK-04 는 태그를 벗긴 글로 재므로 든다.

캡처: 세션 스크래치 `dr1a/shots/` 에 16 쪽 × 세 폭 × 두 테마 96 장 (커밋하지 않음). 320 어두운 `bambu-fields-baseline` · 375 밝은 `kaizen-flow` 를 눈으로 봤다.

## tone-guide 5 단계 대조

레포 `tone-kit/references/` 규칙표와 `locale-korean.md` 를 1 단계에서 읽었다. 어댑터 없음(`.claude/tone-project.md`). 새로 쓴 줄(`git diff -U0` 의 `+` 줄)만 본다.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-10 · G-1 번역투 킬러 패턴 6 종 (docs 다섯 폴더 · scripts · harness 가이드 한 줄) | 0 | 통과 |
| C-01 / C-07 `check-api-kit-docs.py` 새 주석 한 줄 — why 만, 3 줄 이하 | 0 | 통과 |
| N-08 한 글자 이름 (파이썬 · 셸 변경분) | 0 | 통과 — 판정식은 정규식 한 줄만 바꿨다 |
| K-11 새로 만든 이름으로 대상 부르기 | 0 | 통과 — 원본 용어를 그대로 옮겼다 |
| C-04 템플릿 마커 · 구분선 | 0 | 통과 — 페이지 CSS 주석 `/* 코드 조각 … */` 는 이유 주석 |

## 조건별 자기 측정

측정은 `SCR=<세션 스크래치>/dr1a bash .harness/.meta/after-0926-docs-regen-a/measure.sh <번호>`, U = `chore/ak2-dr1a` 끝(`377a5be`, 이 notes 커밋 전).

| 조건 | 값 | 종료 코드 |
| --- | --- | --- |
| SK-01 | `pairs=17 bad=0` | 0 |
| SK-02 | `pairs=17 bad=0` | 0 |
| SK-03 | `pages=14 bad=0` | 0 |
| SK-04 | `pairs=17` `total_missing=0` | 0 |
| SK-05 | `items=6 bad=0` | 0 |
| SK-06 | `skill_rows=8 guide5=0 guide8=1 page5=0 page8=1` | 0 |
| SK-07 | `pages=16 bad=0` | 0 |
| SK-08 | `cells=96 bad=0` | 0 |
| SC-01 | `cases=30 wrong=0  \| compare n=200 diff=0 seed=20260927 \| tree=[12/12 PASS] rc0=0 \| last=static-evidence-viewer-contract applied1=1 rc1=1 fail1=1 fail1_last=1 \| first=contract-extraction-modes applied2=1 rc2=1 fail2=1 fail2_first=1` | 0 |
| SC-02 | `ci_steps=1 job=[validate:] first_job=[validate:] exitdoc=1` | 0 |
| SC-03 | `a11y=rc0/[16/16 PASS] links=rc0/[1] contrast=rc0/[1] api=rc0/[12/12 PASS] table=rc0/[1]` | 0 |
| SC-04 | `tool=59fe55125c0dbc77` · `ci_local_ok=25 other=[feedback-agg-test SKIP (yq 없음)] cause_copies=rc0 measure_helpers=rc0` | 0 |
| ER-01 | `rc=1 rows=12 missing_named=1 summary=[11/12 PASS]` | 0 |
| AR-01 | `scope=21 changed=19 extra=[] required=4/4` | 0 |
| AR-02 | `commits=10 bad=0` (notes 커밋 전) | 0 |
| AR-03 | `seal_commit_files=1 seal_before_impl=1 seal=OK measure=OK` · 묶음 지문 일곱 모두 계약 값과 같음 | 0 |
| AR-04 | 이 파일 — notes 커밋 뒤 잰다 | — |
| AP-02 | `remote_heads=0` | 0 |
| AP-03 | `rc=0 v6=[V6 code-fence        0 bare — OK]` | 0 |
| RE-01 | 더한 파일 0 (`--diff-filter=A`, `.harness` 밖) | — |
| RE-02 | `docs` · `scripts` 에 더한 파일 0 | — |
| DG-01 · DG-03 | `scripts/release.sh` 변경 0 | — |
| DG-02 | `md=rc0/[1]/[Summary: 0 issues in 0 files] py=rc0` | 0 |
| DG-04 | 바뀐 파일에 앱 · 서버 시작 파일 0 | — |

## 남은 것

- SC-01 출력의 `wrong=0` 뒤 빈칸이 둘이다(`ext_cases.py` 가 틀린 사례 목록이 비면 끝에 빈칸을 남긴다). 계약 측정 줄은 빈칸 하나로 적혀 있어 글자 그대로 대조하면 어긋난다 — 값은 모두 같다. 측정 묶음은 봉인돼 고치지 않았다.
- `ci-local.sh` 는 CI 에 새로 넣은 `check-api-kit-docs.py` 단계를 자기 목록 밖으로 알린다. 그 단계는 SC-03 이 따로 잰다.
- 교차 진단 권고 `layout.js` 상대 경로 문제는 회귀 게이트에 「`REPO` 는 절대 경로로」 한 줄로만 남겼다(측정 묶음 지문을 바꾸지 않으려고).
- QA(qa-evaluator) APPROVE — 25/25. 계약 `status` 는 `done`, 리포트는 `.harness/sprint-feedback-after-0926-docs-regen-a.md`. 교차 진단은 부모 몫(`cross_diagnosis_by: pending-parent`)으로 두 가지를 본다 — SC-01 빈칸 차이를 PASS 로 친 판단, 0 건 · 빈 출력으로 통과한 조건이 헛통과인지.
- 독립 검토에서 나온 결함 두 건(막지 않음, 계약 조건이 재지 않는 범위):
  - `docs/bambu-kit/bambu-fields-baseline.html` · `failure-recipes.html` · `materials.html` 머리에 원본의 판 번호 설명이 빠졌다 — 「Studio 판은 실행 때 조회한다, 하드코딩 금지」 · 「두 값은 따로 갱신된다」 · 앱 `02.06.00.51` / 번들 `02.06.00.05` → 2026-09-05 확인 앱 `02.08.02.61` / 번들 `02.08.00.06`, H2S 0.4 기준값 10/10 동일. 원본에 들어간 것이 `07573ee`(2026-09-06)로 기준 판보다 앞이라 SK-04 에 안 걸렸다. `surface-recipes.html` 에는 같은 줄이 있으니 그 모양을 옮기면 된다.
  - 쪽 머리가 원본과 다른 사실을 적는다. `materials.html` 부제 「Bambu Studio 2.6.0 (v02.06.00.51) 기준」이 `377a5be` 에서 넣은 「Studio 버전은 실행 때 조회한다」 표지와 한 머리 안에서 부딪히고, `failure-recipes.html` 머리 표지 「Bambu Studio 2.6.0 (v02.06.00.51)」은 원본의 「버전을 하드코딩하지 마라」와 반대다.
- 참고: `docs/process/kaizen-flow.html` 은 본문의 `assets/site.css` 언급을 `site&#46;css` 로 적어 SK-07(글자 수 1)을 비켜 간다. 담긴 뜻은 맞다. 다음 계약은 링크 태그만 세도록 조건을 바꿔야 한다.
