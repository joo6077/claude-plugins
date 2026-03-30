---
title: 데이터 표시 패턴
version: 0.2.0
last_updated: 2026-03-30
---

# 데이터 표시 패턴

사용자가 데이터를 효율적으로 탐색, 비교, 이해할 수 있도록 돕는 데이터 표시 원칙과 패턴을 정리한다.

---

## 원칙

### 1. 사용자의 핵심 태스크에 맞춰 표시 형태를 결정한다

NNGroup은 데이터 테이블의 4가지 주요 사용자 태스크를 정의한다: (1) 특정 기준에 맞는 레코드 찾기, (2) 데이터 비교, (3) 단일 행 조회/편집/추가, (4) 레코드에 대한 액션 수행. 표시 형태는 이 중 어떤 태스크가 주요한지에 따라 결정해야 한다.

> **출처:** [Data Tables: Four Major User Tasks — NNGroup](https://www.nngroup.com/articles/data-tables/)

### 2. 이미지 중심이면 그리드, 텍스트 중심이면 리스트

NNGroup 연구에 따르면 그리드 뷰는 "시각적 이해와 유사 데이터 타입 구분"에 최적화되어 있고, 리스트 뷰는 "읽기 이해"에 최적화되어 있다. 사용자에게 가장 가치 있는 것이 무엇인지에 따라 선택한다.

> **출처:** [Card View vs. List View — NNGroup](https://www.nngroup.com/videos/card-view-vs-list-view/)

### 3. 모바일에서는 데이터 축소 전략이 필수다

NNGroup은 "큰 화면에서 사용 가능한 테이블을 먼저 만든 후 작은 화면에 맞게 변환"하라고 권장한다. 모바일에서 한 번에 보이는 데이터량이 제한되므로 의미 있는 속성 선정이 데스크톱보다 더 중요하다.

> **출처:** [Mobile Tables: Comparisons and Other Data Tables — NNGroup](https://www.nngroup.com/articles/mobile-tables/)

---

## 리스트/그리드

### 리스트 뷰 (List View)

**적합한 경우:**
- 텍스트 정보가 주요 콘텐츠일 때 (이름, 설명, 가격, 날짜 등)
- 상세 정보와 비교가 중요할 때
- F-패턴 읽기 흐름을 따르는 데이터
- 스크롤을 최소화하고 화면당 더 많은 항목을 보여줘야 할 때

**핵심 설계 규칙:**
- 리스트 항목은 이미지 없이(또는 작은 썸네일만) 더 적은 수직 공간을 차지하여 화면당 더 많은 옵션을 표시할 수 있다
- 정렬(sorting)이 쉽고 공간 효율적이다
- 각 항목에 일관된 레이아웃을 적용: 제목, 부제목, 메타데이터의 위치를 고정한다

> **출처:** [Mobile UX Design: List View and Grid View](https://babich.biz/blog/mobile-ux-design-list-view-and-grid-view/)
> **출처:** [The Anatomy of a List Entry — NNGroup](https://www.nngroup.com/articles/list-entries/)

### 그리드 뷰 (Grid View)

**적합한 경우:**
- 이미지가 주요 콘텐츠일 때 (상품, 갤러리, 포트폴리오)
- 시각적 차이로 항목을 구분할 때
- 탐색/브라우징 중심의 경험

**핵심 설계 규칙:**
- 고품질 이미지가 시각적 참여를 높인다
- 카드 뷰는 효과적인 그룹핑을 생성한다
- **트레이드오프:** 그리드 뷰는 페이지가 길어지고 더 많은 스크롤이 필요하다

> **출처:** [Card View vs. List View — NNGroup](https://www.nngroup.com/videos/card-view-vs-list-view/)
> **출처:** [Image Grids or Text Lists? — NNGroup](https://www.nngroup.com/articles/image-vs-list-mobile-navigation/)

### 뷰 전환 (View Toggle)

두 표시 방식이 모두 유효한 경우, 사용자가 리스트/그리드를 전환할 수 있는 토글을 제공한다. 사용자의 선택을 기억하여 다음 방문 시 유지한다.

---

## 테이블

### 데이터 테이블의 4가지 핵심 태스크

NNGroup이 정의한 데이터 테이블 설계의 기본 프레임워크:

| 태스크 | 필요한 기능 |
|--------|-----------|
| **레코드 찾기** | 필터, 검색, 정렬, 인간이 읽을 수 있는 식별자를 첫 번째 컬럼에 배치 |
| **데이터 비교** | 헤더/컬럼 고정, 지브라 스트라이핑, 호버 하이라이팅, 컬럼 재정렬 |
| **단일 행 조회/편집** | 인라인 편집, 모달 팝업, 비모달 사이드 패널, 아코디언 확장 |
| **레코드 액션** | 단일 레코드 액션 + 체크박스 기반 배치(batch) 액션, "전체 선택" 지원 |

> **출처:** [Data Tables: Four Major User Tasks — NNGroup](https://www.nngroup.com/articles/data-tables/)

### 정렬 (Sorting)

- **(기본) 첫 번째 컬럼은 사람이 읽을 수 있는 레코드 식별자**여야 한다 (자동 생성 ID가 아님)
- 컬럼 배열은 사용자에게 중요한 데이터를 우선 배치한다
- 정렬 방향을 시각적으로 명확히 표시한다 (화살표 아이콘)
- 다중 컬럼 정렬이 필요한 경우를 고려한다

> **출처:** [Data Tables: Four Major User Tasks — NNGroup](https://www.nngroup.com/articles/data-tables/)

### 반응형 테이블 (Responsive Tables)

NNGroup은 "큰 화면에서 사용 가능한 테이블을 먼저 만든 후 작은 화면에 맞게 변환"하라고 권장한다. 모바일에서의 핵심 전략:

**1. 컬럼/행 헤더 고정 (Column Locking)**
수평 스크롤이 필요한 경우, 행 헤더(보통 첫 번째 컬럼)를 고정하여 사용자가 항상 라벨을 볼 수 있게 한다.

**2. 데이터 축소 (Data Reduction)**
- 사용자가 데이터를 보기 전에 필요한 데이터셋을 필터링할 수 있게 한다
- 데이터를 보면서 뷰를 조정할 수 있는 컨트롤을 제공한다

**3. 대안 레이아웃 패턴:**

| 패턴 | 설명 | 적합한 경우 |
|------|------|-----------|
| 수평 스크롤 + 고정 컬럼 | 첫 번째 컬럼을 고정하고 나머지를 스크롤 | 비교가 중요한 테이블 |
| 스택 (카드) 변환 | 각 행을 카드로 변환하여 세로 나열 | 단일 레코드 조회 중심 |
| 컬럼 숨기기 | 중요도가 낮은 컬럼을 숨기고 "더보기"로 접근 | 많은 컬럼, 일부만 핵심 |
| 미니 차트/요약 | 상세 테이블 대신 요약 뷰 제공 | 대시보드, 개요 화면 |

> **출처:** [Mobile Tables: Comparisons and Other Data Tables — NNGroup](https://www.nngroup.com/articles/mobile-tables/)
> **출처:** [How to Fit Big Tables on Small Screens — NNGroup](https://www.nngroup.com/videos/big-tables-small-screens/)

### 시각적 가독성

- **지브라 스트라이핑:** 교대 행 배경색으로 시선 추적을 돕는다
- **호버 하이라이팅:** 마우스 오버 시 행을 강조하여 현재 위치를 명확히 한다
- **테두리/구분선:** 데이터 밀도가 높을수록 시각적 구분이 중요하다
- **숫자 우측 정렬:** 숫자 데이터는 우측 정렬하여 자릿수 비교를 쉽게 한다

---

## 빈 상태/로딩 상태

### 빈 상태 (Empty States)

NNGroup은 빈 상태 설계에 대해 3가지 가이드라인을 제시한다:

#### 1. 시스템 상태를 전달한다

완전히 빈 상태는 사용자에게 혼란을 준다 — 아직 로딩 중인지, 에러가 발생한 것인지, 정말 데이터가 없는 것인지 알 수 없다. "선택한 날짜 범위에 표시할 레코드가 없습니다" 같은 구체적 메시지로 시스템 상태를 명확히 전달한다.

#### 2. 학습 단서를 제공한다

빈 상태는 컨텍스트에 맞는 도움말을 제공할 기회이다. 예를 들어 즐겨찾기 목록이 비어있을 때 "여기에 즐겨찾기를 표시하려면 별 아이콘을 탭하세요"라고 안내한다. 이런 "풀(pull) 방식의 도움"은 강제 튜토리얼보다 기억에 더 잘 남는다.

#### 3. 핵심 태스크로의 직접 경로를 제공한다

빈 상태에 명시적인 행동 유도(CTA)를 포함한다: "생성" 버튼, "더 알아보기" 링크, 또는 데모 데이터로 탐색할 수 있는 옵션 등을 제공하여 사용자가 혼란 없이 다음 단계를 시작하도록 돕는다.

> **출처:** [Designing Empty States in Complex Applications: 3 Guidelines — NNGroup](https://www.nngroup.com/articles/empty-state-interface-design/)

### 로딩 상태: 시간별 표시 전략

NNGroup은 대기 시간에 따라 적절한 로딩 인디케이터를 선택하도록 권장한다:

| 대기 시간 | 권장 인디케이터 | 이유 |
|-----------|---------------|------|
| **< 1초** | 없음 | 빠른 깜빡임은 오히려 방해가 된다 |
| **1~2초** | 스피너 (Spinner) | 시스템이 작동 중임을 알린다 |
| **2~10초** | **스켈레톤 스크린** | 페이지 구조를 미리 보여줘 인지 부하를 줄인다 |
| **> 10초** | 프로그레스 바 | 남은 시간에 대한 감각을 제공한다 |

> **출처:** [Skeleton Screens 101 — NNGroup](https://www.nngroup.com/articles/skeleton-screens/)

### 스켈레톤 스크린 (Skeleton Loading)

스켈레톤 스크린은 "페이지 레이아웃을 모방한 와이어프레임 형태의 시각적 표시"이다. 밝은 회색 박스가 콘텐츠와 이미지를 대표하며, 회색 박스의 구조가 최종 페이지의 구조를 반영한다.

**유형:**

| 유형 | 설명 | 권장 |
|------|------|------|
| **정적(Static) 스켈레톤** | 회색 박스로 콘텐츠/이미지 자리를 표시 | 기본 옵션 |
| **애니메이션(Shimmer) 스켈레톤** | 펄스 또는 시머 효과 추가 | 권장 — 시스템 활성 상태를 전달 |
| **프레임 표시(Frame-display)** | 헤더/푸터만 표시, 콘텐츠 영역 비움 | **비권장** — 사이트 고장으로 오해 가능 |

**핵심 이점:**
- "사이트가 작동하지 않는다는 인식"을 방지한다
- 더 빠른 로딩 체감을 만든다
- 콘텐츠 도착 전에 사용자가 페이지 구조에 대한 멘탈 모델을 형성할 수 있다

**구현 원칙:**
- 스켈레톤의 형태가 실제 콘텐츠 레이아웃과 일치해야 한다
- 개별 모듈(카드, 리스트 아이템)에는 스피너가, 전체 페이지에는 스켈레톤이 적합하다
- 스켈레톤 표시 시간이 10초를 초과하면 프로그레스 바로 전환을 고려한다

> **출처:** [Skeleton Screens 101 — NNGroup](https://www.nngroup.com/articles/skeleton-screens/)
> **출처:** [Skeleton Screens vs. Progress Bars vs. Spinners — NNGroup](https://www.nngroup.com/videos/skeleton-screens-vs-progress-bars-vs-spinners/)
