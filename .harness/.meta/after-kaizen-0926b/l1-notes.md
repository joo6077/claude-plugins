# l1 묶음(design-kit) 마크다운 경고 정리 기록

계약: `.harness/sprint-contract-after-0926-mdlint-l1.md` (봉인 `c6273ee9b186048f` · 측정 지문 `e760f50a17c2d6c9`, 봉인 커밋 `b937756`).
구현 커밋: `80ad7f4` (design-kit 47 파일).

## 경고 수

편집기와 같은 설정(`run.sh` · markdownlint-cli2 0.23.2 · MD013 끔)으로 목록 49 파일을 쟀다.

| 규칙 | 시작 | 자동 고침 뒤 | 끝 |
| --- | --- | --- | --- |
| MD060 | 1554 | 108 | 0 |
| MD032 | 160 | 0 | 0 |
| MD036 | 97 | 97 | 0 |
| MD022 | 50 | 0 | 0 |
| MD040 | 45 | 45 | 0 |
| MD025 | 37 | 37 | 0 |
| MD024 | 10 | 10 | 0 |
| MD031 | 6 | 0 | 0 |
| MD034 | 5 | 0 | 0 |
| MD041 | 1 | 1 | 0 |
| MD029 | 1 | 0 | 0 |
| 합계 | 1966 | 298 | 0 |

손으로 고친 것:

- MD060 108 — 자동 고침이 못 맞춘 표 9 파일은 줄마다 칸 앞뒤 공백 하나(`| a | b |`)로, 구분 줄은 `| --- |` 로 바꿨다
- MD040 45 — 언어 없는 코드 블록은 모두 그림 · 흐름도 · 예시 글이라 `text` 를 붙였다
- MD036 26 — 굵은 글씨 소제목을 바로 위 제목보다 한 단계 아래 제목(`####`)으로 바꿨다. `ethical-design.md` 의 「1단계」 는 경고가 없었지만 2 · 3 단계와 나란히 맞추려고 같이 바꿨다(27 곳)
- 나머지 119 곳 — 규칙을 지키려면 글자를 바꿔야 하는 자리라 그 줄에만 좁혀 껐다(아래 목록)

## 좁힌 끄기 주석

규칙별: MD036 71 · MD025 37 · MD024 10 · MD041 1. 줄 번호는 가지 끝 판에서 주석이 있는 줄이다.

좁힌 끄기 주석: 119

- design-kit/docs/design/accessibility/accessibility.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/accessibility/accessibility.md:120 MD024 다른 상위 절 아래 같은 이름의 소제목이다. 이름을 바꾸면 글자가 바뀐다
- design-kit/docs/design/foundations/animation.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/authentic-design.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/color.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/ethical-design.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/grid-alignment.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/iconography.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/image-illustration.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/information-density.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/microinteraction.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/motion.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/ratio-proportion.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/ratio-proportion.md:74 MD024 다른 상위 절 아래 같은 이름의 소제목이다. 이름을 바꾸면 글자가 바뀐다
- design-kit/docs/design/foundations/ratio-proportion.md:228 MD024 다른 상위 절 아래 같은 이름의 소제목이다. 이름을 바꾸면 글자가 바뀐다
- design-kit/docs/design/foundations/spacing-layout.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/typography.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/visual-hierarchy.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/visual-styles.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/foundations/visual-styles.md:42 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:51 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:83 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:92 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:126 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:135 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:163 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:173 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:208 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:217 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:265 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:274 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:312 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:321 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:356 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:365 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:398 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:407 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:444 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:454 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:489 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:499 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:539 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:549 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:586 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:596 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:639 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:649 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:687 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:697 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:736 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:746 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:784 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:794 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:832 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:842 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:879 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:889 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:938 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:948 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:992 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1002 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1046 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1056 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1096 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1106 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1148 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1157 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1191 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1200 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1233 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1242 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1287 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1296 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1343 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1352 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1399 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1408 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1454 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1464 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1507 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1516 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1558 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1567 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1620 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1630 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1670 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1680 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1725 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/foundations/visual-styles.md:1735 MD036 스타일마다 되풀이하는 라벨이다. 제목으로 바꾸면 같은 제목 35 번이 MD024 로 걸리고, 그건 글자를 바꿔야만 풀린다
- design-kit/docs/design/interaction/data-display.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/interaction/data-display.md:110 MD036 같은 목록의 1 은 굵은 글씨 뒤에 본문이 붙고 3 은 쌍점으로 끝나 제목이 못 된다(쌍점을 지우면 글자가 바뀐다). 2 만 제목으로 바꾸면 나란한 꼴이 깨진다
- design-kit/docs/design/interaction/feedback.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/interaction/forms.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/interaction/navigation.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/systems/apple-hig.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/systems/apple-hig.md:238 MD024 다른 상위 절 아래 같은 이름의 소제목이다. 이름을 바꾸면 글자가 바뀐다
- design-kit/docs/design/systems/apple-hig.md:248 MD024 다른 상위 절 아래 같은 이름의 소제목이다. 이름을 바꾸면 글자가 바뀐다
- design-kit/docs/design/systems/material-design.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/systems/open-source-systems.md:7 MD025 머리 `title:` 이 문서 사이트용 제목이고 본문 첫 `#` 제목이 화면 제목이라 둘 다 둔다. 본문 제목을 한 단계 내리면 파일의 제목 전체가 한 칸씩 밀린다
- design-kit/docs/design/systems/open-source-systems.md:345 MD024 다른 상위 절 아래 같은 이름의 소제목이다. 이름을 바꾸면 글자가 바뀐다
- design-kit/docs/design/systems/open-source-systems.md:388 MD024 다른 상위 절 아래 같은 이름의 소제목이다. 이름을 바꾸면 글자가 바뀐다
- design-kit/docs/design/systems/open-source-systems.md:410 MD024 다른 상위 절 아래 같은 이름의 소제목이다. 이름을 바꾸면 글자가 바뀐다
- design-kit/skills/design-audit/SKILL.md:52 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-audit/SKILL.md:147 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-audit/templates/audit-report.md:37 MD024 틀이 항목 자리를 되풀이해 보여주는 곳이라 같은 제목을 일부러 두 번 쓴다
- design-kit/skills/design-audit/templates/audit-report.md:49 MD024 틀이 항목 자리를 되풀이해 보여주는 곳이라 같은 제목을 일부러 두 번 쓴다
- design-kit/skills/design-component/SKILL.md:31 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-component/SKILL.md:166 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-concept/SKILL.md:90 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-concept/SKILL.md:242 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-guide/SKILL.md:32 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-guide/SKILL.md:84 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-mockup/SKILL.md:35 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-mockup/SKILL.md:192 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-reference/SKILL.md:29 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-reference/SKILL.md:115 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-system/SKILL.md:58 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-system/SKILL.md:146 MD025 레포 SKILL.md 관례대로 `# Process` · `# References` 를 맨 윗단계로 둔다(맨 윗단계 관례 215 줄). 내리면 아래 `##` 단계까지 전부 밀린다
- design-kit/skills/design-test/SKILL.md:14 MD041 스킬 이름은 머리 `name:` 에 있고 본문은 `## Gotchas` 로 시작한다. 맨 윗제목을 새로 넣으면 글자가 늘어난다

## 제목 단계를 바꾼 자리와 읽는 도구

굵은 글씨를 제목으로 바꾼 파일은 7 개다. 제목을 읽는 도구가 있는지 파일 이름으로 찾았다.

명령: `grep -rlF "<파일 이름>" scripts harness/scripts design-kit/evals design-kit/hooks .claude/skills --include='*.py' --include='*.sh' --include='*.json' --include='*.js'`

- design-kit/docs/design/foundations/ethical-design.md — 줄 262 · 266 · 283 을 `####` 로. grep 결과 `design-kit/evals/evals.json` 한 곳, 평가 문장 「ethical-design.md 리서치 문서를 참조한다」 로 파일 이름만 본다. 제목을 읽는 도구 없음
- design-kit/docs/design/foundations/spacing-layout.md — 줄 205 · 209 · 214 · 219 를 `####` 로. grep 결과 `scripts/detect-docs-drift.py:87` 한 곳, 원본 파일을 문서 페이지에 잇는 표라 제목은 안 읽는다. 제목을 읽는 도구 없음
- design-kit/docs/design/foundations/visual-hierarchy.md — 줄 234 · 238 · 242 · 246 을 `####` 로. grep 결과 `design-kit/evals/evals.json` 한 곳, 평가 문장 「visual-hierarchy.md 리서치 문서를 참조한다」 로 파일 이름만 본다. 제목을 읽는 도구 없음
- design-kit/docs/design/foundations/visual-styles.md — 「표면 처리 기반 분류」 · 「검증된 조합」 · 「충돌하는 조합」 · 접근성 1~4 일곱 곳을 `####` 로. grep 결과 0 건. 제목을 읽는 도구 없음
- design-kit/docs/design/systems/material-design.md — 핵심 설계 원칙 1~3 을 `####` 로. grep 결과 0 건. 제목을 읽는 도구 없음
- design-kit/docs/design/systems/open-source-systems.md — 기본 원칙 1~5 를 `####` 로. grep 결과 0 건. 제목을 읽는 도구 없음
- design-kit/skills/design-test/SKILL.md — 「시각 회귀 baseline 검증 루프」 를 `### Step 7` 아래 `####` 로. grep 결과 `scripts/detect-docs-drift.py:49` 한 곳, 문서 페이지 잇기 표라 제목은 안 읽는다. SKILL.md 의 `# Gotchas` 류 절 제목을 찾는 검사도 `grep -rnE "Gotchas|Process|References" --include='*.py' --include='*.sh' scripts harness/scripts design-kit` 로 찾았더니 design-kit 을 읽는 것은 없다(`scripts/sync-orchestrator.py` 는 오케스트레이터 스킬만 읽는다)

맨 윗단계(`#`) 제목은 하나도 바꾸지 않았다. MD025 · MD041 은 좁혀 껐다.

## 검사

- 뜻 검사(`norm.py`): `files=49 changed=47 mismatch=0 disables=119 missing=0`
- 레포 검사 여덟: 모두 종료 코드 0. `design-kit/evals/decision-gate-test.sh` 도 0

## 남은 것

- `python3 scripts/detect-docs-drift.py --since 90d0716` 가 `docs/design-kit/*.html` 28 쪽을 다시 만들 후보로 낸다. 원본 모양만 바뀌어 페이지 내용은 같으니 다시 만들지 않는다(계약 범위 경계)
- `design-kit/references/visual-change-protocol.md` 는 시험 입력이라 손대지 않았다. 이 파일의 경고는 그대로 남아 있다
- 좁힌 끄기 119 곳 가운데 MD025 37 곳(문서 머리 `title:` 과 본문 `#` 제목의 겹침, SKILL.md 의 `# Process` 관례)은 레포 전체 관례를 정하면 한꺼번에 풀 수 있다
