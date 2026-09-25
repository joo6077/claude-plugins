---
title: Tone Kit Research Log
version: 1.0.0
last_updated: 2026-09-25
---

# tone-kit 리서치 로그

`/tone-research` 사이클마다 조회한 1차 출처와 확인 결과를 기록한다. 다음 사이클은 이 로그를 먼저 읽고 같은 소스의 변경분만 확인한다.

## 2026-08-31 — 초기 이관 리서치

**범위:** 킷 생성 시 포지셔닝 인용 교체 + 비공개 출처 대체 + 네이밍 taxonomy 근거 등급 확정

| 카테고리 | 조회 | 결과 |
|---|---|---|
| `stylometry` | arXiv 2507.10583 · SemEval-2026 Task 13 · SANER 2025 | **확인됨.** Droid 는 EMNLP 2025 정식 출판(pp. 31263-31289). SemEval Task 13 Subtask C 가 `Adversarial` 을 별도 클래스로 정의. SANER 2025 는 10개 언어 84.1%±3.8% |
| `stylometry` | DetectGPT · Binoculars | **제외 확정.** 둘 다 자연어 텍스트 탐지기라 코드 스타일 규칙 근거로 범위를 벗어난다 |
| `stylometry` | `effective*` / `resolved*` 접두사 통계 | **확인 실패.** 공개 1차 문헌에 해당 통계 없음. 규칙을 관측 컨벤션으로 격하 |
| `extraction` | Flutter 성능 문서 · StatelessWidget · Element.rebuild · Builder · flutter#149932 | **확인됨.** 공식 문구는 `prefer` 수준이며 `Builder` 라는 공식 인라인 대안이 존재. 비공개 사내 PDF 인용을 이 URL 들로 대체하고 강도를 SHOULD 로 고정 |
| `extraction` | "모든 하위 위젯은 별도 **파일**" | **근거 부재 확인.** 공개 출처는 "different widgets" 까지만 지지하고 "different files" 는 지지하지 않는다. 관측 컨벤션으로 격하 |
| `naming` | M3 · Apple HIG · MUI · Fluent 2 · Ant · Carbon | **판정: 단일 권위 없는 합성.** 6개 시스템이 화면 상단 하나를 4가지 용어로 부른다. 커스텀 컴포넌트 명명 지침을 발행하는 시스템 0개. 접미사 taxonomy 를 합성 규칙으로 라벨 |

**주의로 남긴 것**

- SemEval Task 13 언어 목록이 공식 README 와 overview paper 사이에 PHP/C 표기가 어긋난다. 열거가 필요하면 dataset label 파일로 재확인한다.
- M3 와 Apple HIG 문서는 본문이 JS 로만 렌더링돼 원문 인용을 검증할 수 없다. 어휘 존재 확인용으로만 쓴다.
- SANER 2025 논문의 OpenReview 항목은 프리프린트다. venue 로 표기하면 부정확하다.
- `github.com/flutter/flutter/wiki/Style-guide-for-Flutter-repo` 는 위키 이전 이력이 있어 `sources.md` 에 `주의` 로 표기했다.

**검증 실행**

grep 게이트 10종을 bash·zsh 양쪽에서 실행해 동일 결과를 확인했다. 준수 상태에서 0건이 정상인 익명 레코드 반환 패턴은 합성 양성 케이스 2건 / 음성 0건으로 생존을 증명했다.

## 2026-09-24 — 카이젠 Phase 15 근거 조회

**범위:** 처리 배정표의 `reflect-collector:P6` · `F19`(새 합성어) + 기존 규칙 강도가 출처 강도를 넘는지 재확인 + 현행화. 조회 결과는 카이젠 근거 파일 한 곳에 모였고(본문을 읽은 출처 26 건), 이 사이클은 그 파일만 근거로 썼다.

| 카테고리 | 조회 | 결과 |
| --- | --- | --- |
| `korean` | Microsoft Style Guide · Google Jargon · 한글 맞춤법 제2항 · 제50항 해설 · 국립국어원 다듬은 말 목록 | **K-11 신설, 관측 컨벤션.** 영어권 문서 가이드는 새 말을 만들지 말라고 하고, 한국어 규범은 사전에 없는 전문 용어를 정당하게 본다. 그래서 판정 기준을 사전 등재가 아니라 처음 읽는 사람 기준으로 적었다 |
| `korean` | 국립국어원 etc_seq=663 · LINE 글 | **이름표가 내용보다 넓다.** 663 은 「유형별로 알아보는 보도자료 작성 길잡이」(2021)이고, 본문에서 신조어 · 외래어 지침을 찾지 못했다. LINE 글은 독자 수준과 정보 설계를 다룬다. 둘 다 K-11 근거로 쓰지 않았다. 원칙 1 · 2 · 5 · 8 이 663 을 근거로 드는 문제는 다음 사이클 |
| `comment` | Effective Dart Documentation · 린트 `public_member_api_docs` | **강도 초과 1 건.** C-06 은 MUST 인데 원문 제목은 "PREFER writing doc comments for public APIs" 다. 린트 설명은 "DO document all public members." 라 출처끼리 어긋난다. 이번 사이클은 기록만 한다 |
| `extraction` | Flutter 성능 모범 사례 · `StatelessWidget` · Google Engineering Practices | 변화 없음. prefer · Usually 수준이라 킷 강도(SHOULD)를 넘지 않는다 |
| `stylometry` | Droid (EMNLP 2025) · SemEval-2026 Task 13 | 변화 없음. 규칙 근거로 쓰지 않는 방침 유지 |
| `dart` | Effective Dart Style · 린트 `unnecessary_underscores` · Flutter 3.47.5 · go_router 18.0.1 · `material_ui` | 낡은 곳 목록만 남긴다 — 문서 예시의 `__` 두 곳, 제스처 콜백 58 개의 기준 버전 표기(3.47.5 원본에서도 58 개로 같다), go_router 예제 링크, 위키 스타일 가이드 이전, Material 분리 공지. 다음 사이클 |

**검증 실행.** `core-naming.md` §8 의 표 칸 명령 넷(G-1 · G-2 · G-5 · G-6)이 죽어 있었다. 표 칸에서는 `|` 를 `\|` 로 적어야 하는데, 그 글을 그대로 붙여 넣으면 `\|` 가 정규식의 "또는" 이 아니라 글자 `|` 로 읽힌다. bash · zsh 둘 다 G-1 · G-2 · G-5 는 합성 양성 케이스에서 0 건(종료 코드 1 — 문서가 통과로 읽는 값)이었고, G-6 은 파이프 자리의 `\|` 가 인자로 넘어가 파일의 모든 줄을 냈다. 명령을 코드 블록으로 옮겼다.

확장자 변수를 한 문자열로 두면 확장자가 둘일 때 zsh 가 나누지 않아 0 건이 되는 것도 확인했다. `core-naming.md` §8 · `core-comment.md` §6 · 개요 문서 예시의 확장자 변수를 배열로 바꿨다. 나머지 게이트 25 종은 bash · zsh 모두 합성 양성 케이스를 잡았다.
