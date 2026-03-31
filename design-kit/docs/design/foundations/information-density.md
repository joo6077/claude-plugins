---
title: 정보 밀도
version: 0.2.0
last_updated: 2026-03-30
---

# 정보 밀도

화면에 얼마나 많은 정보를 담을지 결정하는 원칙, 플랫폼별 전략, 조절 기법, 안티패턴을 정리한다.

---

## 원칙

### 1. Data-Ink Ratio를 극대화한다

Edward Tufte는 "The Visual Display of Quantitative Information"에서 Data-Ink Ratio 개념을 제안했다. 그래픽에서 데이터를 전달하는 잉크의 비율을 최대화하고, 장식적 요소(non-data-ink)를 최소화하라는 원칙이다. 수식으로 표현하면:

```
Data-Ink Ratio = 데이터 전달 잉크 / 전체 잉크
```

3D 효과, 배경 이미지, 불필요한 테두리, 과도한 그리드 라인은 모두 non-data-ink다. 이를 제거하면 정보 전달 효율이 올라간다.

> **출처:** [InfoVis Wiki — Data-Ink Ratio](https://infovis-wiki.net/wiki/Data-Ink_Ratio)

### 2. 데이터 밀도를 두려워하지 않는다

Tufte는 높은 데이터 밀도를 오히려 권장한다. "데이터 밀도"는 그래픽 면적당 데이터 항목 수로 정의된다. 하나의 그래픽에 여러 차원의 데이터를 보여주면 패턴과 맥락을 동시에 파악할 수 있다. 핵심은 "많은 데이터"가 아니라 "많은 관련 데이터"를 보여주는 것이다.

> **출처:** [The Double Think — Tufte's Principles](https://thedoublethink.com/tuftes-principles-for-visualizing-quantitative-information/)

### 3. 점진적 공개(Progressive Disclosure)로 복잡성을 관리한다

NNGroup에 따르면 점진적 공개(Progressive Disclosure)는 학습 용이성, 사용 효율, 오류율 세 가지 사용성 지표를 개선한다. 처음에는 가장 중요한 옵션만 보여주고, 사용자 요청에 따라 추가 정보를 공개하는 방식이다. 1차 정보와 2차 정보의 분류가 정확해야 효과가 있다.

> **출처:** [NNGroup — Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)

### 4. 맥락이 밀도를 결정한다

동일한 데이터라도 사용 맥락에 따라 적절한 밀도가 달라진다. 의사 결정을 위한 대시보드는 높은 밀도가, 온보딩 화면은 낮은 밀도가 적합하다. "밀도가 높다 = 나쁘다"라는 편견을 버려야 한다.

---

## 밀도 스펙트럼

### Sparse(저밀도) ↔ Dense(고밀도) 스펙트럼

```
[Sparse]                                                    [Dense]
  온보딩     마케팅     블로그     설정      리스트     테이블     대시보드     IDE
  ←────────────────────────────────────────────────────────────────────→
  탐색·감상                  일상 사용                   전문가·분석
```

| 밀도 수준 | 여백 비율 | 화면당 정보량 | 적합한 사용자 |
|-----------|-----------|--------------|--------------|
| **Very Sparse** | 60–70% | 1–3개 핵심 메시지 | 첫 방문자, 신규 사용자 |
| **Sparse** | 40–50% | 3–5개 섹션 | 일반 소비자 |
| **Moderate** | 25–35% | 5–10개 항목 | 반복 사용자 |
| **Dense** | 15–20% | 10–30개 항목 | 숙련 사용자 |
| **Very Dense** | 5–10% | 30개+ 항목 | 전문가, 파워 유저 |

### 밀도 선택 기준

| 질문 | 저밀도 | 고밀도 |
|------|--------|--------|
| 사용자가 초보인가? | O | X |
| 의사결정이 필요한가? | X | O |
| 비교가 필요한가? | X | O |
| 감성적 경험이 중요한가? | O | X |
| 반복 사용하는가? | X | O |
| 모바일인가? | O | X |
| 스캔 속도가 중요한가? | X | O |

---

## 플랫폼별 전략

### 모바일 — 집중(Focused)

- **화면당 하나의 주요 작업**에 집중한다
- 리스트 아이템 높이: 56–72dp (Material), 44–60pt (iOS)
- 터치 타겟 최소 44x44pt (Apple HIG), 48x48dp (Material)
- 스크롤은 허용하되, 핵심 정보는 첫 화면에 배치

```
[모바일 밀도 예시]
┌─────────────────┐
│   Search Bar     │  ← 하나의 입력
│─────────────────│
│  Item 1          │  ← 1줄 제목 + 보조 텍스트
│  Item 2          │
│  Item 3          │
│  Item 4          │     높이 72dp/아이템
│  Item 5          │
│  Item 6          │
│─────────────────│
│  Bottom Nav      │
└─────────────────┘
```

> **출처:** [Apple HIG — Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

### 태블릿 — 적당(Moderate)

- 2컬럼 Master-Detail 패턴이 기본
- 좌측 리스트 + 우측 상세 정보
- 리스트 영역은 모바일과 유사한 밀도, 상세 영역은 데스크톱에 가까운 밀도
- iPad 가로 모드에서 Split View가 자연스러운 밀도 분배를 제공

### 데스크톱 — 밀집(Dense)

- max-width 1200px 기준으로 3–4단 레이아웃 가능
- 사이드바 + 메인 + 보조 패널 구조
- 리스트 아이템 높이: 40–56dp (compact mode 가능)
- hover 상태를 활용한 detail-on-demand
- 키보드 단축키로 밀집 정보 탐색 지원

### 대시보드 — 초밀집(Very Dense)

- KPI 카드 + 차트 + 테이블이 한 화면에 공존
- 핵심 수치는 크게(Display/Headline), 세부 데이터는 작게(Body/Label)
- 컬러를 이상치(anomaly) 표시에만 사용
- 필터로 표시 범위를 조절할 수 있게 한다

```
[대시보드 밀도 예시]
┌──────┬──────┬──────┬──────────────────┐
│ KPI1 │ KPI2 │ KPI3 │   Alert Banner   │
│ 1.2M │ 94%  │ +12% │                  │
├──────┴──────┴──────┤──────────────────┤
│                    │                  │
│   Line Chart       │   Pie Chart      │
│                    │                  │
├────────────────────┴──────────────────┤
│  Data Table (20+ rows visible)        │
│  Compact row height: 36–40px          │
└───────────────────────────────────────┘
```

---

## 콘텐츠 유형별 밀도

### 기사/블로그

- 행당 글자 수: 50–75자 (영문), 25–35자 (한글)
- line-height: 1.5–1.8
- 단락 간격: 본문 행간의 1.5–2배
- 이미지로 텍스트 밀도를 분산

### 데이터 테이블

- 기본 행 높이: 52dp (Material), compact: 36dp
- 열 간격(padding): 16dp
- 셀 내 텍스트는 좌측 정렬(텍스트), 우측 정렬(숫자)
- 행 수가 20개 이상이면 고정 헤더(sticky header) 필수
- 줄무늬 배경(striped rows)은 밀집 테이블에서 행 추적을 돕는다

### 설정 화면

- 그룹 헤더로 카테고리 구분
- 토글, 드롭다운 등 컨트롤은 우측 정렬
- 설명 텍스트는 선택적 표시(필요시 펼치기)
- 섹션 간격: 32–48dp, 항목 간격: 0–1dp (구분선 사용)

### 폼

- 필드 간격: 16–24dp
- 라벨-필드 간격: 4–8dp
- 선택 필드와 필수 필드의 시각적 구분
- 긴 폼은 섹션으로 분할하고 진행 표시기 사용

---

## 밀도 조절 기법

### 1. 여백 조절

가장 직접적인 밀도 조절 방법이다. padding과 margin 값을 줄이면 밀도가 올라가고, 늘리면 내려간다.

| 밀도 모드 | 컴포넌트 패딩 | 아이템 간격 |
|-----------|-------------|-----------|
| **Comfortable** | 16dp | 8dp |
| **Cozy** | 12dp | 4dp |
| **Compact** | 8dp | 0dp (구분선) |

Gmail은 사용자가 직접 밀도 모드(Default, Comfortable, Compact)를 선택할 수 있게 한다.

### 2. 그룹핑

관련 요소를 시각적으로 묶으면 개별 항목이 아닌 "그룹 단위"로 스캔할 수 있어 체감 밀도가 줄어든다.

- **카드**: 관련 정보를 하나의 컨테이너에 담기
- **구분선**: 가벼운 그룹 분리
- **섹션 헤더**: 그룹 라벨 제공
- **탭**: 동일 공간에서 카테고리 전환

### 3. 접기/펼치기 (Collapse/Expand)

- Accordion: 하나의 섹션만 펼치고 나머지는 접기
- Expandable Row: 테이블 행을 클릭하면 상세 정보 표시
- Read More: 긴 텍스트의 처음 2–3줄만 표시

### 4. Detail-on-Demand

마우스 hover, 클릭, 롱 프레스 시 추가 정보를 표시한다.

- **Tooltip**: 간략한 설명 (1–2줄)
- **Popover**: 중간 수준의 상세 정보
- **Bottom Sheet / Drawer**: 풍부한 상세 정보
- **새 화면 이동**: 완전한 상세 정보

### 5. 필터와 검색

표시할 데이터 자체를 줄여 밀도를 관리한다. 대시보드에서 날짜 범위 필터, 테이블에서 컬럼 표시/숨기기, 리스트에서 카테고리 필터가 대표적이다.

### 6. 사용자 제어 밀도

전문 도구(IDE, 스프레드시트, 이메일 클라이언트)에서는 사용자가 직접 밀도를 조절할 수 있게 하는 것이 좋다.

```
[밀도 설정 예시]
View > Density
  ○ Comfortable (기본)
  ○ Cozy
  ○ Compact
```

---

## 안티패턴

### 과잉 여백 (Too Sparse)

| 증상 | 결과 |
|------|------|
| 카드 하나에 정보 2줄 | 스크롤 과다, 탐색 비효율 |
| 화면의 60% 이상이 빈 여백 | 공간 낭비, "이게 전부인가?" 느낌 |
| 한 화면에 CTA 하나 | 정보를 얻으려면 계속 다음 화면으로 이동 |
| 불필요한 전체화면 히어로 이미지 | 스크롤 없이는 실질 콘텐츠에 도달 불가 |

Tufte는 "chartjunk"을 비판하면서도 데이터를 숨기는 과잉 단순화 역시 비판했다. 정보를 보여줘야 할 곳에서 여백만 보여주는 것은 사용자의 시간을 낭비하는 것이다.

### 과잉 밀집 (Too Dense)

| 증상 | 결과 |
|------|------|
| 구분 없이 50개+ 항목이 나열 | "정보의 벽" — 어디서 시작할지 모름 |
| 텍스트 크기가 모두 12px | 계층 구조 부재로 스캔 불가 |
| 여백 없이 요소가 접촉 | 클릭/터치 타겟 겹침, 오조작 |
| 10개+ 컬럼의 테이블 | 수평 스크롤 필수, 맥락 상실 |
| 동시에 3개+ 차트 표시 | 어디에 주목해야 할지 불명확 |

### 밀도 불일치

동일 화면 내에서 영역별 밀도가 극단적으로 다르면 혼란을 유발한다. 헤더가 초저밀도인데 바로 아래 본문이 초고밀도이면 시각적 충돌이 발생한다. 점진적 밀도 변화(sparse → moderate → dense)가 자연스럽다.

---

## 밀도 감사 체크리스트

| # | 점검 항목 | 판단 기준 |
|---|-----------|-----------|
| 1 | 화면당 주요 작업이 명확한가? | 1–3개의 핵심 행동이 식별 가능 |
| 2 | 스크롤 없이 핵심 정보를 파악할 수 있는가? | Above the fold에 KPI/제목/CTA 존재 |
| 3 | 그룹핑이 되어 있는가? | 관련 정보가 카드/섹션으로 묶임 |
| 4 | 사용자 유형에 맞는 밀도인가? | 초보자용은 sparse, 전문가용은 dense |
| 5 | 플랫폼에 맞는 밀도인가? | 모바일은 focused, 데스크톱은 dense |
| 6 | non-data-ink가 최소화되었는가? | 장식적 테두리, 3D 효과, 배경 패턴 제거 |
| 7 | progressive disclosure가 적용되었는가? | 2차 정보는 요청 시 공개 |
| 8 | 밀도 전환이 점진적인가? | 영역 간 밀도 차이가 급격하지 않음 |

---

## 참고 문헌

- [Edward Tufte — The Visual Display of Quantitative Information](https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/)
- [InfoVis Wiki — Data-Ink Ratio](https://infovis-wiki.net/wiki/Data-Ink_Ratio)
- [NNGroup — Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)
- [Material Design 2 — Understanding Layout](https://m2.material.io/design/layout/understanding-layout.html)
- [Apple HIG — Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
