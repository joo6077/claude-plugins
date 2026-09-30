# rest — 남은 작은 결함 모음 기록

- 계약: `.harness/sprint-contract-after-0929-leftovers.md` (28 조건, 봉인 커밋 839bdd74, 측정 도우미 커밋 15d5480d)
- 작업 폴더: `.claude/worktrees/ak3-rest`, 가지 `chore/ak3-rest`, 시작 판 ab637374
- 봉인 전 교차 진단이 빠진 항목 하나를 짚었다 — fs2 QA 2 · 3 회차가 연속으로 낸 「범위 목록 × CI 전용 단계」 점검. 항목 (12) · 구조-11 로 계약에 넣은 뒤 봉인했다.

## 항목별 결과

| 항목 | 한 일 | 커밋 |
| --- | --- | --- |
| (1) prd-patterns 날짜 | 원본 `last_updated` 와 쪽 두 자리 날짜를 2026-09-29 로. 드리프트가 짚은 ADR 경계 절의 질문 셋 · 적용 시점 · 한계도 쪽에 실었다 | 07e7131b · 88226611 |
| (2) Gotcha 10 번호 겹침 | setup-guide 원본의 `1. ①` ~ `5. ⑤` 를 `- ①` ~ `- ⑤` 로 | 10cf0ec1 |
| (3) Phase 4 두 확인 | 원본 · 쪽 Phase 4 에 「출처 줄 두 날짜 확인」 · 「서비스 계정 키 안내 확인」 단계를 더해 둘 다 9 단계 | 10cf0ec1 · a43261f8 |
| (4) A10 둘째 몫 | `docs/planning/flows.md` 의 Mermaid 문장을 A10 교체안대로(비시험판 · GitHub 릴리스 주소 · npm `latest` · 렌더해 확인하지 않았다). 쪽의 「최신 안정판」 여섯 자리도 맞추고 날짜를 커밋 날로 | 07e7131b · 88226611 |
| (5) check-docs-common-css media 속성 | `<style media=…>` · `<link media=…>` 의 `prefers-reduced-motion` 도 잡는다. `media="print"` 는 통과. 시험 경우 7 을 더해 7/7 | 22104d4f |
| (6) check-api-kit-docs 연결 판정 | `rel` 에 `stylesheet` 가 있고 주소가 `assets/site.css` 로 끝나는 `<link>` 만 연결로 센다. 새 시험 `scripts/test-check-api-kit-docs.py` 다섯 경우, CI 등록 | 22104d4f · 000da1ae |
| (7) 테마 단추 | howto-kit 여섯 쪽에 `id="theme-btn"` 단추를 품은 `nav` 를 넣었다(쪽에 이미 있던 `.nav` · `.theme-toggle` 스타일과 `applyTheme` 이 찾는 `#theme-icon` · `#theme-label` 을 그대로 씀). 본문 배경 전환 효과는 뺐다 — 아래 「판단」 참조 | e59dc715 |
| (8) 스크립트 움직임 | `docs/design-kit/animation.html` 스프링 공 · 깜빡임 상자, `docs/design-kit/data-display.html` 진행 막대에 `matchMedia('(prefers-reduced-motion: reduce)')` 확인을 넣어 줄이기 설정에서는 끝 상태를 바로 보인다 | a30d64f1 |
| (9) 쪽 없는 원본 둘 | `docs/reflect-kit/memory-grounding.html` · `docs/reflect-kit/reflect-kaizen.html` 을 fs2 변환기로 만들고 목차 · 아이콘에 올렸다. 판정 표 · 이웃 문서 절을 더했다 | 9bc7eec2 · 27098ec8 |
| (10) 드리프트 다시 보기 | `--since cacd9da3` 짝 열하나 모두 새 낱말 · 인라인 코드를 쪽이 싣는다(setup-guide 쪽 76 낱말 · prd-patterns 쪽 24 낱말을 원본 문장대로 옮김) | a43261f8 · 88226611 |
| (11) sprint-contract Gotcha | 봉인 전 기존 검사 대조(grep · 사본 · 「더하라」 · 「그대로」 · 겹침) 한 줄 | be32dce8 |
| (12) 범위 목록 × CI 전용 단계 | `harness/docs/guides/contract-design-guide.md` 에 `### 범위 목록과 CI 전용 단계 맞대기 (2026-09-29 추가)` 절, 쪽 `docs/harness/contract-design-guide.html` 같은 자리에 같은 절 | be32dce8 · 233e7b96 |

## 판단

- 테마 단추만 넣었을 때 구조-03 이 여섯 쪽 가운데 다섯 쪽에서 `bg_differs=0` 이었다. 쪽 CSS 가 본문 배경에 0.25 초 전환 효과를 걸어 두어, 누른 직후에는 배경색이 아직 옛 값이다(직접 재 보니 누른 직후 `rgb(13, 13, 20)`, 0.6 초 뒤 `rgb(244, 245, 249)`). 봉인된 측정을 느슨하게 하지 않고, docs-site 정본 틀(`.claude/skills/docs-site/references/page-template.html`) 의 `body` 에 전환 효과가 없는 것에 맞춰 여섯 쪽의 본문 전환 줄만 뺐다. 그 뒤 두 번 재어 6/6.
- 가이드 `version` · `last_updated` 는 올리지 않았다. 올리면 `qa-evaluation-guide.md` §버전 정보 Parity 까지 같이 올려야 한다. 새 절 제목의 `(2026-09-29 추가)` 표시로 남겼다.

## 킷 버전 판단

- harness — `harness/skills/sprint-contract/SKILL.md` Gotcha 한 줄과 가이드 절 하나가 바뀌어 patch 대상이다.
- onboarding-kit — `setup-guide` 스킬의 Phase 4 단계가 늘어 patch 대상이다.
- planning-kit · design-kit · howto-kit · reflect-kit — 레포 뿌리 `docs/` 쪽만 바뀌어 킷 파일 변화가 없다. 올리지 않는다.
- 릴리스는 이 묶음 밖이다. 합친 뒤 `main` 에서 `scripts/release.sh` 로 올린다.

## tone-guide

- 1 단계: 레포 `tone-kit/references/` 의 코어 넷과 `locale-korean.md` 를 읽었다. 오버레이 `.claude/tone-project.md` — 어댑터 없음, 주석 언어 ko. 걸리는 규칙은 C-01 · C-07 · N-08 · S-03 · S-04 · K-02 · K-04.
- 5 단계: 바뀐 줄(`.harness` · 새 쪽 제외)에서 번역투 여섯 모양 grep 0 건(K-02). 새 코드의 한 글자 이름은 0 건이고, 걸린 셋(`s` · `t` · `p`)은 봉인 지문이 걸린 측정 도우미 `jsmotion.js` 안이라 고치지 않았다(N-08 SHOULD). 새 주석(쪽 스크립트 셋 · 검사 스크립트 둘)은 모두 「왜」 를 적는다(C-01). pass-through 래퍼 없음(S-04) — 새 쪽 설정 파일은 fs2 `gen.py` 의 `render` 를 그대로 부른다.

## 남긴 것

- `scripts/check-docs-common-css.py` 의 `site.css` 링크 세기는 여전히 `rel` 을 보지 않는다 — fs2 가 남긴 두 항목 밖이라 계약 「하지 않는 것」 대로 두었다. api-kit 쪽 검사와 같은 판정(`links_site_css`)으로 맞추면 된다.
- 본문 배경에 전환 효과가 걸린 쪽이 howto-kit 밖에 40 쪽 남아 있다(api-kit 12 · tone-kit 10 · design-kit 6 · flutter-toolkit 6 · infra-kit 4 · backend-kit 2). 이 쪽들은 이미 단추가 있어 이번 범위가 아니다. 같은 측정(fs2 `br.js theme`)으로 재면 누른 직후 배경이 같다고 나올 수 있다 — 쪽을 고칠지, 측정이 전환 끝을 기다리게 할지 정해야 한다.
- Mermaid 예시를 12 에서 실제로 렌더해 확인하는 일은 하지 않았다(원본 문장이 그렇게 적는다).
- QA 판정은 APPROVE(28 조건 중 PASS 25 · N/A 3). 리포트와 계약 `status: done` 은 커밋 d2b71d8e 에 담았다.
- 독립 검토가 넘긴 약점 셋. 막는 결함은 아니라 이번에 고치지 않았다 — 고치기 전 판정도 똑같이 통과시키던 모양이라 전보다 나빠진 것이 없고, 지금 api-kit 13 쪽은 모두 `<link rel="stylesheet" href="../assets/site.css">` 한 모양이라 실제로 틀리게 판정되는 쪽이 없다. 봉인 뒤 판정을 더 좁히면 계약 범위 밖 변경이 된다.
  - `scripts/check-api-kit-docs.py` 의 `links_site_css` 가 가짜 연결 넷을 연결로 친다. `data-rel="stylesheet" rel="preload"`(정규식 `\brel` 이 `data-rel` 에 먼저 걸린다), `data-href="../assets/site.css" href="x.css"`(같은 이유로 `\bhref`), `rel="alternate stylesheet"`, `media="print"`. 속성 앞에 `(?<![-\w])` 를 붙이고 alternate · media 를 따로 보면 된다. 새 시험 `scripts/test-check-api-kit-docs.py` 에 이 넷을 음성 경우로 더한다.
  - 같은 판정이 이제 `href="../assets/site.css?v=2"` 처럼 물음표 값이 붙은 주소를 연결 없음으로 본다. 예전엔 연결로 셌다. 판정이 엄격해진 쪽이고 시험 경우 · 문서 어디에도 적혀 있지 않다 — 받아들일지 정해 시험 경우로 못박는다.
  - `scripts/check-docs-common-css.py` 에 새로 넣은 media 속성 검사는 넣어 본 네 모양(글자 참조로 쪼갠 값 · 따옴표 없는 값 · `<script>` 안 문자열 · `<source media>`)에서 문제가 없었다. 남길 일 없음.
