# 컨셉 도출 기준

design-concept 스킬이 참조하는 컨셉 도출 카테고리와 기준.

## 무드 키워드 분류

| 축 | 예시 키워드 |
|----|-------------|
| 온도 | warm, cool, neutral |
| 무게감 | light, bold, heavy |
| 형식성 | formal, casual, playful |
| 복잡도 | minimal, rich, dense |
| 시대감 | classic, modern, futuristic |

3-5개 키워드를 선정하여 프로젝트의 디자인 톤을 정의한다.

## 컬러 방향 체계

컨셉 단계에서는 구체적 hex 값이 아닌 **방향**만 정의한다:

| 요소 | 정의 내용 | 예시 |
|------|-----------|------|
| 톤 계열 | warm/cool/neutral | "따뜻한 뉴트럴 베이스" |
| 채도 수준 | muted/vivid/mixed | "전반적으로 muted, 포인트만 vivid" |
| 포인트 방향 | 강조색의 역할과 느낌 | "에너지를 주는 오렌지 계열 포인트" |
| 다크 모드 방향 | 다크 모드의 성격 | "순수 검정 아닌 다크 그레이 베이스" |

> **참조:** `docs/design/foundations/color.md` — 컬러 시스템 원칙
> **참조:** `docs/design/foundations/authentic-design.md` — 제네릭 컬러 방지

## 타이포그래피 선택 기준

| 요소 | 선택지 | 고려 사항 |
|------|--------|-----------|
| 서체 분류 | sans-serif / serif / mono / mixed | 프로젝트 성격, 가독성 |
| 본문 서체 | 시스템 폰트 / 웹폰트 | 로딩 성능, 브랜드 |
| 제목 서체 | 본문과 동일 / 대비 서체 | 시각 위계, 브랜드 개성 |
| 웨이트 활용 | 2단계(regular/bold) / 3단계+ | 위계 표현 필요도 |

> **참조:** `docs/design/foundations/typography.md` — 타이포그래피 원칙

## UI 패턴 카테고리

| 카테고리 | 선택지 |
|----------|--------|
| 레이아웃 기본 형태 | 카드 그리드 / 리스트 / 매거진 / 대시보드 |
| 네비게이션 패턴 | 탭바 / 사이드바 / 햄버거 / 탑바 |
| 정보 밀도 | 낮음(여백 중심) / 중간 / 높음(데이터 중심) |
| 카드 스타일 | 플랫 / 엘리베이션 / 보더 / 글래스모피즘 |
| 버튼 스타일 | 필드 / 아웃라인 / 텍스트 / 라운드 |
| 인풋 스타일 | 언더라인 / 아웃라인 / 필드 |

> **참조:** `docs/design/systems/material-design.md` — Material Design 패턴
> **참조:** `docs/design/systems/apple-hig.md` — Apple HIG 패턴
> **참조:** `docs/design/systems/open-source-systems.md` — 오픈소스 디자인 시스템 패턴
