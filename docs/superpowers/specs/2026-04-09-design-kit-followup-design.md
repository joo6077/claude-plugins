# design-kit 후속 작업 설계

## 개요

design-kit 템플릿 인프라 구축 완료 후 후속 작업. 구조 정리 → 스킬 개선 → visual-styles 퀄리티 개선 → 정리.

## Phase 1: 구조 정리

### 1-1. 스킬 내부 templates/ → 공유 templates/ 통합

4개 스킬의 내부 templates/ 디렉토리를 삭제하고 SKILL.md에서 공유 `design-kit/templates/` 경로를 참조하도록 변경.

| 스킬 | 삭제 대상 | 참조 변경 |
|------|-----------|-----------|
| design-concept | skills/design-concept/templates/ | ../../templates/moodboard.html |
| design-reference | skills/design-reference/templates/ | ../../templates/catalog.html |
| design-mockup | skills/design-mockup/templates/ | ../../templates/mockup.html |
| design-component | skills/design-component/templates/ | ../../templates/component.html |

### 1-2. design-kit/references/visual-styles.md 생성

35종 스타일 구조화 데이터. 속성 레이어 분리 (구조/질감/컬러/타이포) — 조합 가능 형태. 스킬(concept, mockup)이 스타일 요청 시 참조.

### 1-3. sync-docs 실행

SKILL.md 변경 반영.

## Phase 2: 스킬 리서치 기반 개선 (3개 병렬)

### 2-1. design-concept

- 리서치: 무드보드 작성 베스트 프랙티스, 디자인 디렉션 문서 패턴
- Gotchas 보강 (4개 → 7~9개)
- 산출물 섹션 구조 정의 (design-component 수준으로)

### 2-2. design-reference

- 리서치: 디자인 레퍼런스 수집/큐레이션 패턴, 벤치마크 분석 방법론
- Gotchas 보강
- 카탈로그 산출물 구조 정의

### 2-3. design-mockup

- 리서치: 하이파이 시안 프레젠테이션 패턴, A/B 비교 방법론
- Gotchas 보강
- 시안 산출물 구조 정의

각각: 리서치 → SKILL.md 개선 → sprint contract → QA evaluator

## Phase 3: visual-styles 퀄리티 개선

### 3-1. 실무 레퍼런스 리서치

- Dribbble/Behance/Awwwards 등에서 각 스타일별 실제 프로덕션 수준 레퍼런스 수집
- 모달 컴포넌트(버튼/카드/인풋)가 실무에서 어떻게 스타일링되는지 분석
- 스타일별 핵심 시각 특성 정리 — "이게 진짜 이 스타일이다"

### 3-2. 35종 카드 데모 퀄리티 리워크

- 각 스타일의 카드 배경/질감/그림자/타이포가 실무 레퍼런스 수준으로 차별화
- 색상만 바뀌는 게 아니라 레이아웃/텍스처/분위기까지 다르게

### 3-3. 35종 모달 컴포넌트 퀄리티 리워크

- 버튼/카드/인풋이 해당 스타일의 실무 레퍼런스 반영
- Playwright로 전수 시각 검증

### 3-4. QA

sprint contract → QA evaluator → Playwright 전수 검증

## Phase 4: 정리

- `.playwright-mcp/` 삭제
- 불필요 플랜 파일 정리
- 최종 커밋
