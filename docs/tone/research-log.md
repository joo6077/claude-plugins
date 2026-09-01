---
title: Tone Kit Research Log
version: 1.0.0
last_updated: 2026-08-31
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
