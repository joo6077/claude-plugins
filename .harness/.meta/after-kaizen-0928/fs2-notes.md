# fs2 기록 — 문서 사이트 밝은 테마 · 움직임 규칙 · 드리프트

계약 `.harness/sprint-contract-after-0929-final-sweep-docs.md` (봉인 `sha256:34da4f58f14e406f` · 측정 `sha256:e2e8c0f8d4737f10`,
봉인 커밋 `87500fcc`, 측정 도우미 커밋 `94174ada`). 개정 `.harness/sprint-amendments-after-0929-final-sweep-docs.md`
AM-01 (커밋 `ccf33dee`).

## 1 회차에서 멈춘 까닭과 개정

구조-03 은 시작 판 202 쪽의 색 지문이 그대로이길 요구하는데, 지문은 글자를 가진 요소마다 한 줄이라 요소를 더하면
색이 같아도 바뀐다. 구조-07 의 목차 항목 둘(`docs/index.html`)과 구조-08 의 원본 내용 채우기
(`docs/bambu-kit/bambu-print-profile.html`)가 요소를 더해야 해서 세 조건을 함께 만족할 수 없었다.
사용자가 2026-09-29T04:43:11.908Z (세션 bda55d45 기록 6392 번째 줄) 에 두 쪽만 「새로 더한 요소를 뺀 나머지 요소의
색은 시작 판과 같다」로 좁혀 재는 개정에 동의했다. 개정 측정은 `keep-colors-narrow.py` · `br-rows.js` 다.

## 항목별 처리 커밋

| 항목 | 커밋 | 한 것 |
| --- | --- | --- |
| 밝은 테마 118 쪽 | `42579355` (공통 파일) · 킷 폴더 커밋 `aaab5ccb` `e09c21b7` `e1a0a353` `576b4edb` `1e34bae3` `21f87c68` `caf4a154` `c828e095` `6eddf2f0` `9a2a3870` `8e4159b6` `216e2b7b` `84bcfce8` `2edc3e7b` `4d504397` · 검사기 `5a7e7fa3` · 새 쪽 즉시 전환 `a4dd0a1b` `fd026e0b` | 쪽에 단추 · 저장 · 복원 스크립트를 넣고, 공통 파일이 `:root:has(.dk-theme-btn)[data-theme="light"]` 에서 색 변수를 밝은 값으로 바꾼다. 쪽에 박힌 색은 `var(--dk-ink-out, 원래 값)` 꼴. 접근성 검사기는 두 테마로 칠한 모양을 비교해 밝은 테마를 알아본다 |
| 움직임 줄이기 106 쪽 | `42579355` · 같은 킷 폴더 커밋 · 검사 `5a7e7fa3` · 스킬 글 `ed37f581` | 쪽 안 규칙을 지우고, 가리킬 때 `transform` 130 곳을 `var(--dk-hover-move, 원래 값)` 으로 바꿨다. 공통 CSS 검사가 쪽 `<style>` 의 규칙을 잡는다(시험 경우 6) |
| research-log (디자인 연구 기록) | `2edc3e7b` (새 쪽 · 목차) · `5a7e7fa3` (드리프트 매핑) · `ed37f581` (스킬 표) | `docs/design/research-log.md` → `docs/design-kit/research-log.html` |
| 드리프트 다시 보기 | 킷 폴더 커밋 · `4d504397` (새 쪽 `docs/react-kit/style-guide.html`) · bambu 쪽 채우기 `e1a0a353` `61b5b91e` `80e70d73` | 31 짝 모두 `OK`. bambu 쪽은 1.95.3 전송 경로 · Phase 3.1 · 프린터 설정 검사 발췌 · 시험 파일 실행 줄 · 오르카 확인 절차 · 체크리스트 35 ~ 38 을 새 요소로 더했다 |
| 그 밖 | `471461b3` | 구조-10 이 잡은 `docs/design-kit/design-template.html` 의 레포 밖 글꼴 링크 둘을 뺐다(시작 판부터 있던 것) |

도구 폴더 `.harness/.meta/after-0929-final-sweep-docs/tools/` — `add_theme_button.py` · `strip_motion.py` ·
`wrap_hover_move.py` · `fix_light_ink.py` · `gen.py`(dr2 변환기를 옮김) · `pages.py` · `page.css`. 새 쪽 body 색 전환을
뺀 것은 `page.css` 에도 옮겼다. bambu 쪽 채우기는 scratch 의 `fill_bambu.py` 로 했다(기존 요소 글은 건드리지 않음).

## tone-guide 1 · 5 단계

- 1 단계: 레포 `tone-kit/references/` 의 `core-comment.md` (C-01 ~ C-17) · `core-naming.md` (N-01 ~ N-12) ·
  `core-structure.md` (S-01 ~ S-14) · `core-antipatterns.md` (A ~ J) · `locale-korean.md` (K-01 ~ K-11) 규칙표를 읽었다.
  오버레이 `.claude/tone-project.md` 가 있다. 어댑터는 dart-flutter 뿐이라 이번 대상(Python · JS · HTML · CSS)은 코어만.
- 5 단계 대조 — 대상: 스킬 글 추가 줄, bambu 쪽 추가 줄, 공통 파일 · 검사 스크립트 추가 줄, 개정 측정 두 파일, 도구 폴더.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 · K-10 §8 G-1 번역투 여섯 가지 | 0 | 통과 — `git diff cacd9da3` 추가 줄과 새 파일에 grep |
| C-10 디자인 툴 참조 · C-13 자화자찬 헤더 | 0 | 통과 |
| C-01 · C-07 주석은 까닭만 · 3 줄 이하 | 0 | 통과 — `br-rows.js` 의 폭 돌리기 주석, `keep-colors-narrow.py` 의 docstring 은 까닭(같은 상태에서 읽기 · 짝 맞추는 규칙) |
| N-08 한 글자 이름 | 0 | 새로 쓴 두 측정 파일에 없음. `measure.py` 의 옛 이름은 봉인 판이라 두었다 |
| S-04 넘기기만 하는 래퍼 | 0 | 통과 |

## 이 묶음 밖으로 남긴 것

- 이미 두 테마인 84 쪽 가운데 단추 없는 두 테마 쪽 6 개 — 대상은 어두운 테마만 있던 쪽이다
- 스크립트로 주는 움직임(`behavior:'smooth'` 스크롤 등) — 공통 파일이 멈출 수 없다
- 합쳐지지 않은 묶음 fs1 — 합친 뒤 드리프트는 그 판에서 다시 본다
- 쪽 없는 원본 둘(`reflect-kit/references/memory-grounding.md` · `reflect-kit/skills/reflect-kaizen/SKILL.md`) — 네 항목 밖
