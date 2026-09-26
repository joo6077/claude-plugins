# dcb 묶음 기록 — 문서 사이트 새 페이지 일곱

계약: `.harness/sprint-contract-after-0926-docs-new-pages.md` (봉인 커밋 `e495e2f`, 조건 25, 봉인 지문 `sha256:d6913d6663e9d866`).
가지 `chore/ak2-dcb`, 시작 판 `6378948`.

## 항목별 결과

| 항목 | 결과 | 커밋 |
| --- | --- | --- |
| DC-1 대응 페이지 없는 원본 다섯 | 새 쪽 다섯을 만들고 킷 목차에 올림 | `49e017c` · `e9b5fc1` · `9a6af50` · `74b4810` · `3709432` · `74f67fd` · `71b7a92` |
| UD-4 나머지 원본 둘 | 새 쪽 둘, 일곱째 원본의 드리프트 매핑 한 줄과 매핑 표 한 행 | `77ce08d` · `930bdba` · `71b7a92` |
| 처리됨 | 없음 — 시작 판에 일곱 모두 쪽 파일과 목차 등록이 없었다 | — |
| 바깥 근거 대기 | 없음 | — |

- DC-1 다섯 원본은 드리프트 도구가 이미 이 쪽 이름을 내고 있어서 쪽 이름을 그대로 따랐고, 목차 등록과 파일이 생기자 도구 코드를 고치지 않고도 짝이 맞았다.
- UD-4 의 일곱째 원본은 드리프트 도구에 매핑이 아예 없어서 폴더째가 아니라 그 파일 하나만 `docs/process/` 로 이었다. 같은 폴더의 `phase-dependencies.md` · `search-sources.md` 는 쪽이 없어서 폴더째 이으면 거짓 새 쪽으로 뜬다.
- 목차 id 는 DC-1 쪽마다 원본 이름을 따랐고, Rust Kit 쪽만 flutter-toolkit 이 이미 쓰는 `project-detection` 과 겹치지 않게 `project-detection-rust` 로 정했다. API Kit 쪽은 같은 킷의 다른 id 들처럼 `api-` 를 붙여 `api-research-log` 로 했다.
- 쪽 모양: 틀의 색 토큰 · 넘침 규칙 네 가지 · `dk-theme` 테마 전환을 그대로 쓰고, 밝은 테마에서는 킷 색을 어둡게 바꿔 글자 대비를 맞췄다. 어두운 테마 `--text3` 은 틀 값 대신 docs-site Gotcha 14 가 정한 `#948779` 를 썼다. 테마 단추 id 는 레포 접근성 검사가 크기를 재는 `theme-btn` 이다.
- 쪽 본문은 원본 md 를 줄 순서 그대로 옮긴 변환 결과이고, 그 위에 손으로 쓴 머리글 · 요점 카드 넷 · 목차, 아래에 출처 주소 모음을 붙였다. 변환에 쓴 스크립트는 세션 임시 폴더에만 두고 커밋하지 않았다.

## 다른 묶음과 부딪히는 곳 · 넘긴 것

- 매핑 표 `process (공유)` 행: 이 묶음은 원본 칸에 `phase-research-templates.md` 를 더했고, 다른 묶음 vsa 의 VS-13 도 같은 행을 고친다. 합칠 때 이 한 줄이 부딪히며, 합친 행에는 오케스트레이터 `SKILL.md` 와 `phase-research-templates.md` 두 원본을 모두 남겨야 한다.
- 목록 DC-9 매핑 규칙 결정 가운데 `process (공유)` 원본 칸을 오케스트레이터 `SKILL.md` 로 두는 몫은 VS-13 이 같은 줄에서 하므로, 이 묶음의 더하기와 뜻이 맞선다고 보지 않았고 합친 행에 둘 다 남는지만 부모가 보면 된다.
- 드리프트 도구 쪽은 vsa 가 고친 둘레가 아니라 onboarding 매핑 바로 아래 두 줄에 더해서 부딪히지 않을 것으로 본다.
- 원본을 고칠 다른 묶음이 합쳐진 뒤 드리프트 도구로 다시 맞춰야 하는 쪽: reflect-digest 는 VS-21 이 원본 한 줄을 이미 고쳤다. project-detection 은 KR-1 과 KR-3 이 고칠 예정이다. phase-research-templates 는 VS-16 과 VS-17 과 VS-26 이 고칠 예정이다. 이 묶음은 시작 판 `6378948` 원본으로 만들었다.
- 그 묶음들이 합쳐진 뒤 `python3 scripts/detect-docs-drift.py --since <합친 기준>` 을 돌리면 이제 짝이 있으니 새 쪽이 아니라 다시 맞출 쪽으로 나온다.
- 검사 스크립트 `check-api-kit-docs` 는 연구 기록 원본을 건너뛰고, 시작 판에서도 이미 12 쪽 가운데 0 쪽만 통과한다. VS-14 몫이라 이 묶음은 기대지 않았다.
- 320 폭 레포 검사기는 DC-2(dca 묶음)가 레포 접근성 검사에 넣는 일이고, 이 묶음은 계약 도우미로 320 · 375 · 1280 폭과 두 테마를 따로 재서 42 칸 모두 넘침 0 을 확인했다.
- 틀의 `--text3` 대비와 단추 id 고침도 dca 몫이라 틀 파일은 건드리지 않았다.

## 확인한 값

| 조건 | 값 |
| --- | --- |
| SK-01 | `minus=1 plus=1 nonrow=0 outside_step1=0` · `seven_in_table=7/7` |
| SC-01 | `seven_ok=7/7` |
| SC-02 | `delta_n=1 excludes_same=1` (일곱째 원본 하나) |
| SC-03 | `seven_in_table=7/7 mismatch=0->0` |
| ER-01 | `of_ok=7/7 cells_zero=42/42` |
| ER-02 | `absent=0` · `a11y_rc=0 ok_both=7/7` |
| ER-03 | `nav_ok=7/7 console_err=0` |
| AR-01 | `added=7/7` · `exist=7/7 lines=7/7 css1=7/7 ext0=7/7 accent=7/7` |
| AR-02 | `reg_ok=7/7 icon_ok=7/7 dup_ids=0->0 added=14 deleted=0` · `links_rc=0` |
| AR-03 | `cov_ok=7/7` (낱말 0.98 ~ 1.00, 코드 표시 전부 1.00) |
| AR-04 | `url_ok=7/7 src_urls_total=108` |
| AR-05 | `hide0=7/7` |
| AR-06 | `extra=0 missing=0 png=0 status=A7 M3` · `seal_broken=0` |
| AR-07 | `multi_docs_folder=0 mixed=0`, 구현 커밋 9 |
| RE-02 | `theme=7/7 light=7/7 rm0=7/7` · `new_scripts=0` |
| DG-02 | `tag_worse=0 md_skill=9->9 py_compile=0 cli_rc=0` |

## 킷별 버전 판단

없음. 바꾼 파일은 문서 사이트 `docs/` · 레포 스크립트 `scripts/detect-docs-drift.py` · 레포 전용 스킬 `.claude/skills/docs-site/SKILL.md` 뿐이고 플러그인 킷 폴더는 한 파일도 바꾸지 않았으므로 올릴 판이 없다.

## 문서 드리프트

`python3 scripts/detect-docs-drift.py --since 6378948` 출력은 `no docs drift since 6378948` 이다. 원본 md 는 하나도 바꾸지 않았고, 새로 이은 짝 일곱은 계약 도우미 SC-01 로 따로 확인했다.

## tone-guide 결과

tone-guide 1 단계: `.claude/tone-project.md` 오버레이(어댑터 없음, 주석 언어 ko)를 읽고 코어 넷(`core-comment.md` · `core-naming.md` · `core-structure.md` · `core-antipatterns.md`)과 `locale-korean.md` 를 이 워크트리 판으로 읽었다. 어댑터가 없어 스택 고유 grep 검사는 꺼진 채 진행했다.

tone-guide 5 단계 전수 대조 — 대상은 새 쪽의 손으로 쓴 글(머리글 · 요점 카드 · 고정 문구), 드리프트 도구 주석 한 줄, 매핑 표 한 행, 이 기록 파일이다.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 why 만 남긴다 | 0 | 통과 — 도구 주석은 폴더째가 아니라 파일 하나만 잇는 이유 한 줄 |
| C-02 이름 반복 | 0 | 통과 |
| C-04 템플릿 마커 · 구분선 | 0 | 통과 |
| C-13 자화자찬 헤더 | 0 | 통과 |
| C-15 주석 종결형 | 0 | 통과 — 도구 주석은 단문 |
| N-09 무역할 파일명 | 0 | 통과 — 쪽 이름은 원본 이름 그대로 |
| S-01 ~ S-14 구조 | 0 | 해당 없음 — 커밋한 코드는 매핑 두 줄뿐 |
| K-02 번역투 여섯 가지 (G-1) | 1 → 0 | 「그대로 적용된다」 한 건을 「그대로 걸린다」 로 고침. 남은 히트 한 건은 번역투 여섯 가지를 예로 든 카드라 자기모순 검사 예외 |
| K-03 능동형 · 직설 | 0 | 통과 |
| K-04 종결형 | 0 | 통과 — 쪽 글과 기록 모두 한다체 |
| K-05 외래어 | 0 | 통과 |
| K-06 이름 번역 주석 | 0 | 해당 없음 |
| K-10 대조 grep 실행 | 1 회 | G-1 을 손으로 쓴 글 전부에 돌림. G-2 ~ G-4 는 `///` 문서 주석 대상이라 해당 없음 |
| K-11 새로 만든 이름 | 0 | 통과 — 요점 카드 제목은 원본 절 이름이나 하는 일을 풀어 씀 |

같은 과정에서 사용자 전역 쉬운 말 목록에 걸리는 낱말(게이트 · 승격)을 요점 카드에서 풀어 썼다(`74b4810` · `3709432` · `74f67fd`). 원본에서 옮긴 본문 글은 원본 표기를 그대로 둔다.

## 캡처

캡처 폴더: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/dcb/cap`

새 쪽 일곱 × 320 · 375 · 1280 폭 × 두 테마 = 42 장을 커밋하지 않고 위 폴더에 두었고, 여러 장을 직접 열어 겉모습과 밝은 테마 대비를 눈으로 봤다.

## 측정 도구

- 계약 측정 도우미: 계약 `## 회귀 게이트` 블록을 떼어 쓴다(`m <조건 ID>`).
- 로컬 자동 검사: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh`.
- 원본 담김 비교: 같은 폴더의 `coverage.py` · `fence2.py` (AR-03 알려진 답 대조에 씀).

## 남은 것

- 옛 값 검사 `check-stale-values` 가 오케스트레이터 참고 문서 폴더를 검사 대상에 넣지 않는다. 등록 킷 폴더와 문서 폴더만 훑기 때문이며 목록 VS-27 과 같은 모양이다. 이 묶음이 고치면 계약의 허용 파일 밖이라 새 남은 일 후보로 부모에게 넘긴다.
- 매핑 표 `process (공유)` 행의 합칠 때 부딪힘과, 원본을 고칠 다른 묶음이 합쳐진 뒤 세 쪽(reflect-digest · project-detection · phase-research-templates)을 다시 맞추는 일은 위 절에 적은 대로 부모가 모아서 한다.
