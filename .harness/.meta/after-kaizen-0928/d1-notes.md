# d1 기록 — 문서 사이트 약점 (A2 · A3 · B12 · B13 · B14 · B15 · B16 · B17 · D3 · D5)

계약: `.harness/sprint-contract-after-0928-docs-site.md` (봉인 커밋 `c6b8cf4`, 31 조건). 가지 `chore/ak3-d1`, 시작 판 `e500a63`. 측정 도우미 커밋 `0dd9a45`.

## 항목별 결과

| 항목 | 한 일 | 커밋 |
| --- | --- | --- |
| A2 | 짝 다섯을 드리프트 도구의 덮어쓰기 매핑으로 기존 쪽에 이었고, tone `project-detection.md` 는 도구가 건너뛴다. 새 쪽 열셋을 만들고 목차에 등록했다. `--since 6378948 --include-format-only` 출력의 NEW 표지가 19 → 0 이 됐다 | `005a695` · `72358a1` · `5c48e6c` · `eb20291` · `6151944` · `78ba356` · `ef30083` · `b6a6cb2` · `0e77de4` · `6803188` · `8be644a` |
| A3 | 일곱 쪽에 밝은 테마 · `theme-btn` 단추 · `dk-theme` 저장 · 브라우저 색 설정 따르기를 넣었다. 제목 그러데이션 · 배지 · 코드 색처럼 어두운 배경에 맞춰 박힌 색은 밝은 테마 규칙을 따로 두었다 | `eb20291` · `78ba356` · `47f1148` · `6144e87` · `b593ba1` |
| B12 | `search-strategy.html` 의 `G1~G4` 를 `G1~G5` 로 고쳤다 | `b593ba1` |
| B13 | bambu 세 쪽에 원본 머리의 「판 번호는 실행 때 조회」 안내(`Info.plist` · `BBL.json` · 최초 판 · 2026-09-05 확인 판)를 싣고, 판 번호가 보이는 줄에 「최초 작성 때」 를 붙였다 | `5c48e6c` |
| B14 | `setup-guide.html` 이 원본 인라인 코드 82 개를 모두 싣고, 「만들 수 없다고 결론 낼 때도 네 칸」 규칙 문장을 싣는다 | `b593ba1` |
| B15 | `design-test.html` 의 기능 카드 들뜸을 `@media (prefers-reduced-motion: no-preference)` 안으로 옮겼다 | `47f1148` |
| B16 | dr2 가 다시 쓴 쪽 열에 옛 판 형제 링크를 「같은 킷의 이웃 쪽」 카드로 되살리고, react 다섯 쪽에 손 글 절 아홉을 지금 스킬에 맞춰 다시 썼다 | `6151944` · `78ba356` · `672cc4b` |
| B17 | 세 쪽의 숫자 글자 참조를 원래 글자로 바꾸고, 공통 CSS 링크를 `<link>` 요소로 세는 새 검사와 시험을 CI 에 넣었다 | `005a695` · `3ddcca4` · `72358a1` · `78ba356` · `c274f34` |
| D3 | 드리프트 도구가 모양만 바뀐 원본을 기본으로 빼고(뺀 짝 수를 표준 오류에 적음) `--include-format-only` 로 모두 보인다. 내용이 바뀐 짝 가운데 쪽이 못 따라간 여덟 쪽을 원본 새 문장에 맞췄다. 임시 저장소 시험을 CI 에 넣었다 | `005a695` · `3ddcca4` · `72358a1` · `5c48e6c` · `6151944` · `6144e87` · `c274f34` · `280bff7` |
| D5 | 아래 결정표로 원본 27 개의 지금 결정을 다시 적었고, 옛 표(dca DC-9)에는 정정 한 줄만 달았다 | 이 기록과 같은 커밋 |

## 원본별 결정표 (D5)

「새 페이지」 는 그 원본에 쪽이 따로 있다는 뜻이고, 「짝」 은 이름이 다른 기존 쪽에 잇는다는 뜻이다. 드리프트 도구의 매핑과 목차가 이 표와 같다 (`m AR-05` 가 파일 · 목차 · 도구 출력과 맞대 본다).

| 원본 | 결정 | 근거 |
| --- | --- | --- |
| `bambu-kit/skills/bambu-print-profile/references/comment-analysis.md` | 새 페이지: `docs/bambu-kit/comment-analysis.html` | 같은 폴더의 다른 참고 문서는 모두 쪽이 있다 (DC-9 와 같음) |
| `bambu-kit/skills/bambu-print-profile/references/tolerance.md` | 새 페이지: `docs/bambu-kit/tolerance.html` | 위와 같음 |
| `bambu-kit/skills/bambu-print-profile/references/user-preferences.md` | 새 페이지: `docs/bambu-kit/user-preferences.html` | 위와 같음 |
| `flutter-toolkit/references/figma-parity-self-verify.md` | 새 페이지: `docs/flutter-toolkit/figma-parity-self-verify.html` | 같은 폴더의 참고 문서 넷은 모두 같은 이름의 쪽이 있다 (DC-9 와 같음) |
| `harness/references/cross-kit-principles.md` | 새 페이지: `docs/harness/cross-kit-principles.html` | harness 참고 폴더에서 이 문서만 쪽이 없었다 (DC-9 와 같음) |
| `react-kit/references/clean-arch-layout.md` | 새 페이지: `docs/react-kit/clean-arch-layout.html` | react 참고 폴더 원칙 (DC-9 와 같음) |
| `react-kit/references/common-gotchas.md` | 새 페이지: `docs/react-kit/common-gotchas.html` | 위와 같음 |
| `react-kit/references/result-patterns.md` | 새 페이지: `docs/react-kit/result-patterns.html` | 위와 같음 |
| `reflect-kit/skills/reflect-promote/SKILL.md` | 새 페이지: `docs/reflect-kit/reflect-promote.html` | 스킬마다 한 쪽 원칙 (DC-9 와 같음) |
| `docs/flutter/research-log.md` | 새 페이지: `docs/flutter-toolkit/research-log.html` | DC-9 는 「페이지 없음이 맞음」 이었지만 아래 「research-log 방향」 절의 까닭으로 바꿨다 |
| `docs/planning/research-log.md` | 새 페이지: `docs/planning-kit/research-log.html` | 위와 같음 |
| `docs/rust/research-log.md` | 새 페이지: `docs/rust-kit/research-log.html` | 위와 같음 |
| `docs/tone/research-log.md` | 새 페이지: `docs/tone-kit/research-log.html` | 위와 같음. DC-9 가 든 「레포 안내가 tone 리서치 문서 여덟 종을 셀 때 조사 기록을 뺀다」 는 셈 규칙일 뿐 쪽을 막지 않는다 |
| `tone-kit/references/core-antipatterns.md` | 짝: `docs/tone-kit/antipattern-catalog.html` | 같은 주제의 리서치 쪽이 먼저 있었다 — 이름으로 두 번째 쪽을 만들지 않는다 (Gotcha 7 · RE-02) |
| `tone-kit/references/core-comment.md` | 짝: `docs/tone-kit/comment-economy.html` | 위와 같음 |
| `tone-kit/references/core-naming.md` | 짝: `docs/tone-kit/naming-taxonomy.html` | 위와 같음 |
| `tone-kit/references/core-structure.md` | 짝: `docs/tone-kit/extraction-thresholds.html` | 위와 같음 |
| `reflect-kit/skills/codex-kaizen/references/search-sources.md` | 짝: `docs/reflect-kit/codex-kaizen.html` | 스킬의 부속 목록이라 그 스킬 쪽에 묶는다 (DC-9 와 같음) |
| `tone-kit/references/project-detection.md` | 페이지 없음 | 킷이 프로젝트 값을 감지하는 절차라 읽을 쪽으로 옮기지 않는다. 도구 `SOURCE_EXCLUDES` 가 건너뛴다 |
| `docs/api/research-log.md` | 새 페이지: `docs/api-kit/research-log.html` | 사용자 결정 DC-1 로 만들어졌다(`e9b5fc1`). DC-9 의 「페이지 없음이 맞음」 은 지금 사실과 다르다 |
| `docs/backend/research-log.md` | 새 페이지: `docs/backend-kit/research-log.html` | dr2 가 DC-1 선례를 따라 만들었다(`31942a4`) |
| `docs/infra/research-log.md` | 새 페이지: `docs/infra-kit/research-log.html` | dr2 가 만들었다(`c95c5fa`) |
| `docs/react/research-log.md` | 새 페이지: `docs/react-kit/research-log.html` | dr2 가 만들었다(`1fa06a2`) |
| `tone-kit/references/adapter-contract.md` | 새 페이지: `docs/tone-kit/adapter-contract.html` | DC-1 이 새 쪽으로 정했다. DC-9 의 「페이지 없음이 맞음」 은 지금 사실과 다르다 |
| `tone-kit/references/adapter-dart-flutter.md` | 새 페이지: `docs/tone-kit/adapter-dart-flutter.html` | DC-1 이 새 쪽으로 정했다. DC-9 의 「짝: dart-flutter-idioms」 는 지금 사실과 다르다 |
| `tone-kit/references/locale-korean.md` | 새 페이지: `docs/tone-kit/locale-korean.html` | DC-1 이 새 쪽으로 정했다 |
| `tone-kit/references/sources.md` | 새 페이지: `docs/tone-kit/sources.html` | DC-9 표에 없던 원본이라 dr2 가 새 쪽으로 만들었다 |

### research-log 방향 — 넷을 지우지 않고 넷을 더 만든 까닭

- DC-9 결정표는 dca 서브에이전트가 정했다(`4bee454`, 2026-09-26 21:10 KST). research-log 행의 근거 「다른 킷도 조사 기록 페이지가 없다」 는 같은 날 앞서 나온 **사용자** 결정 DC-1(2026-09-26T10:30:16.222Z, 19:30 KST)과 부딪힌다.
- DC-1 의 범위는 기록마다 다르게 적혀 있다. `after-kaizen-0926b/decisions.md:17` 은 「대응 페이지 없는 원본 일곱」 이라 적었고, `after-kaizen-0926b/leftovers.md:202` 는 그 다섯에 api 연구 기록을 넣었다. 어느 쪽이든 api 연구 기록은 사용자 결정으로 쪽을 받았다 — 그 쪽은 DC-9 16 분 뒤(`e9b5fc1`, 21:26 KST) 생겼다.
- 사용자 결정이 서브에이전트 결정보다 앞서므로 DC-9 의 research-log 행을 틀린 행으로 봤다. 이미 있는 넷을 지우면 내용을 잃고, 남은 넷을 만들면 킷마다 같아진다. 그래서 넷을 더 만들었다.

## 톤 규칙 대조 (`tone-guide`)

1 단계(규칙 로드) — 레포 `tone-kit/references/` 의 `core-comment.md` · `core-naming.md` · `core-structure.md` · `core-antipatterns.md` · `locale-korean.md` 규칙표를 읽었다. 오버레이 `.claude/tone-project.md` 는 어댑터 없음 · 주석 언어 ko 다. 이번 변경에 걸리는 규칙: C-01 · C-02 · C-04 · C-07 · C-13 · C-15, N-08 · N-09, S-03 · S-04 · S-06, K-02 · K-03 · K-04 · K-10 · K-11, 카탈로그 A · B · F · H.

5 단계(완료 전 대조) — 대상은 새로 쓴 스크립트 넷(`scripts/detect-docs-drift.py` 바뀐 부분 · `scripts/test-detect-docs-drift.py` · `scripts/check-docs-common-css.py` · `scripts/test-check-docs-common-css.py`), `.claude/skills/docs-site/SKILL.md` 에 더한 글, CI 주석, 이 기록이다.

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-10 §8 G-1 번역투 여섯 | 0 | 통과 — 양성 대조: 목적격 조사 뒤에 「처리」 와 「한다」 를 붙인 합성 문장 한 줄을 같은 정규식이 1 건으로 잡았다 |
| C-04 · F 구분선 블록 | 0 | 통과 — 새 스크립트에 `# ----` 류 없음 |
| C-13 자화자찬 헤더 | 0 | 통과 |
| C-01 · C-02 what 주석 | 0 | 통과 — 남긴 주석은 「왜」 뿐이다 (예: 글자 수로 재면 본문 언급이 섞인다, 한쪽 판에 파일이 없으면 내용이 바뀐 것으로 본다) |
| N-08 한 글자 이름 | 0 | 통과 — 새 스크립트의 이름은 `page` · `text` · `links` · `splits` · `repo` 등 |
| N-09 무역할 파일명 | 0 | 통과 |
| S-04 넘기기만 하는 래퍼 | 0 | 통과 — `shown()` 은 경로를 레포 기준으로 바꾸는 일을 한다 |
| S-06 헬퍼 체인 | 0 | 통과 |
| K-11 새로 붙인 이름 | 0 | 통과 — 「모양만 바뀐 원본」 은 정의를 도움말과 스킬 문서에 함께 적었다 |
| H 좋은 주석 보존 | — | 도구의 기존 주석(2026-09-14 · 2026-09-25 사고 기록)은 지우지 않았다 |

## 이 묶음 밖으로 남긴 것

- **어두운 테마만 있는 118 쪽** — 로컬 CI `docs-a11y` 로그에서 `theme=dark-only` 118 줄(전체 202 쪽). A3 일곱은 이번에 고쳤고 새 쪽 열셋은 처음부터 두 테마다. 나머지는 목록 A3 의 대상이 아니라 두고 간다.
- **쪽 `<style>` 안에 움직임 줄이기를 다시 적은 쪽 106 개** — 시작 판 105 개에 B15 의 `design-test.html` 이 하나 더했다. 그 쪽의 규칙은 공통 파일이 맡는 전환 시간 줄이기와 달리 가리킬 때 들뜸(transform)을 움직임 허용 때만 주는 규칙이라, docs-site Gotcha 1 에 이 경우를 적었다. 새 검사 `check-docs-common-css.py` 는 이것을 막지 않는다 — 막으면 CI 가 떨어지고, 105 쪽 정리는 이 묶음의 항목이 아니다.
- **접근성 검사기가 `themeToggle` 단추를 못 재는 것(B7)**, **로컬 CI 도구(D2)**, **변환 스크립트를 레포에 들이기(D4)** — 다른 항목이다. 이번 새 쪽도 세션 임시 폴더의 변환 스크립트(dr2 것을 고쳐 씀: 본문 글자 참조 치환 제거 · body 배경 전환 제거)로 만들었다.
- **AR-03 에서 옛 판과 달라진 곳** — 되살린 손 글은 지금 `react-kit/skills/` 와 `docs/react/kit-design/` 에 맞춰 다시 썼다. 사람이 대조한 결과:
  - 옛 판의 규칙 번호 `AP-01` · `AP-02` · `AP-10` · `AP-11` · `AP-40` 은 지금 `/react-audit` 에 없다. 여섯 카테고리 이름(Library Policy · Architecture · Strict TypeScript · Performance 등)으로 바꿨다.
  - 애니메이션 금지 목록이 여섯에서 열한 종으로 늘었다 (`react-dnd` · `react-beautiful-dnd` · `@formkit/auto-animate` · `animate.css` · `react-transition-group` 추가).
  - 커밋 전 검사가 실패하면 「git stash 로 이전 성공 지점 복원」 이던 옛 문장은 지금 스킬에 없다. 지금은 실패한 단계에서 즉시 멈추고 나머지를 안 돌렸다고 보고한다. 공유 작업 폴더에서 stash 는 남의 변경을 삼키므로 되살리지 않았다.
  - deep 감사의 에이전트 넷이 옛 판(react-reviewer · widget-inspector-react · animation-architect-react · 보안 react-reviewer)과 다르다. 지금은 react-reviewer 셋(관점별) + widget-inspector-react 하나다.
  - TanStack Router 플러그인이 `TanStackRouterVite()` 에서 `@tanstack/router-plugin` 의 `tanstackRouter()` 로, shadcn 초기화가 `npx shadcn@latest init` 에서 `pnpm dlx shadcn@latest init --template vite` 로 바뀌었다.
  - 옛 판의 번들 크기 수치(motion 약 50 kB 등), 「감사 결과는 tag 기반 캐시」, 「이동 뒤 eslint」 는 지금 스킬에 근거가 없어 뺐다. G3 좋은 예의 `<Spinner />` 는 Skeleton 규칙과 부딪혀 `<ImageSkeleton />` 으로 바꿨다.
  - `.react-audit-baseline.json` 모드 · `vitest run` · passed · skipped 두 수 보고는 옛 판에 없던 지금 규칙이라 더했다.

## 킷 버전 판단

바꾼 파일은 레포 문서 사이트(`docs/`), 레포 스크립트(`scripts/`), CI 파일, 레포 전용 스킬(`.claude/skills/docs-site/`)뿐이다. 플러그인 폴더(`*-kit/` · `harness/` · `flutter-toolkit/`) 안의 파일은 하나도 바꾸지 않았으므로 킷 버전을 올릴 것이 없다.

## 측정 결과 (자기 측정, HEAD 기준)

- `m SC-01` `pairs_ok=5/5 drift_rc=0` · `m SC-02` `new_marks=0 no_page_lines=0 lines=190 drift_rc=0` · `m SC-03` `all=190 default=56 expect_real=56 only_tool=0 only_ref=0 rc=0,0` · `m KA` `caching=SHAPE tone_overview=REAL`
- `m AR-01` `new_pages_ok=13/13` · `m AR-02` `ok=20/20` · `m AR-03` 열 줄 `OK` · `m AR-04` `pairs=56 bad=0 drift_rc=0` · `m PAGES` `bad=0` · `m EXT` `ext_pages=0`
- `m ER-01` 세 줄 `OK` · `m ER-03` `G1~G4=0 G1~G5=1` · `m ER-04` 세 줄 `OK` `loose_version_lines=[]` · `m ER-05` `code=82/82 rule_sentence=1 miss=[]` · 카드 측정 `reduce … transform=none` · `no-preference … matrix(1, 0, 0, 1, 0, -2)`
- 새 시험: `test-detect-docs-drift.py` 경우 3 개 통과(음성 대조 — 가름을 늘 「내용 바뀜」 으로 바꾼 사본은 경우 1 FAIL · 종료 코드 1), `test-check-docs-common-css.py` 경우 5 개 통과(음성 대조 — 글자 참조 세기를 지운 사본은 경우 2 FAIL, 주석 빼기를 지운 사본은 경우 3 FAIL, 둘 다 종료 코드 1)
- 로컬 CI 25 단계 `rc=0`(yq 없는 `feedback-agg-test` SKIP), `docs-a11y` `202/202 PASS`. CI 파일에만 있는 단계와 새 셋 · `npx playwright test`(164 passed) 모두 종료 코드 0

## 남은 것

- QA 판정(qa-evaluator)과 계약 `status: done` 은 이 묶음이 하지 않는다 — 부모가 판정을 돌린다.
- 이 가지를 `chore/after-kaizen-0928` 에 합친 뒤에는 다른 ak3 묶음이 바꾼 원본이 있어 드리프트를 그 판에서 다시 봐야 한다 (계약 `## 범위 경계` 둘째 항목).
- 위 「이 묶음 밖으로 남긴 것」 다섯(118 쪽 밝은 테마 · 106 쪽 스타일 정리 · B7 · D2 · D4)은 까닭과 함께 다음 목록으로 넘긴다.
