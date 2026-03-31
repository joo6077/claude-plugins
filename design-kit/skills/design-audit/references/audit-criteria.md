# 디자인 감사 기준

design-reviewer 에이전트가 참조하는 카테고리별 체크리스트.

## Typography

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 스케일 일관성 | 정의된 타이포 스케일 외 임의 크기 미사용 | Material Design 3 Typography |
| 행간 비율 | line-height가 font-size의 1.2~1.6배 | WCAG 1.4.12 |
| 최소 크기 | 본문 텍스트 14px(모바일) / 16px(웹) 이상 | Apple HIG Typography |

## Color

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 대비 비율 | 텍스트/배경 대비 WCAG AA (4.5:1 이상) | WCAG 2.1 SC 1.4.3 |
| 시맨틱 사용 | 하드코딩된 컬러값 대신 시맨틱 토큰 사용 | Material Design 3 Color |
| 다크 모드 | 다크 모드에서도 대비 비율 유지 | Apple HIG Dark Mode |

## Spacing

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 스케일 일관성 | 정의된 스페이싱 스케일 외 임의 값 미사용 | EightShapes Space in DS |
| 터치 타겟 | 인터랙티브 요소 최소 44×44pt | Apple HIG Accessibility |
| 여백 일관성 | 같은 레벨의 요소는 동일 간격 | Gestalt 근접성 원칙 |

## Accessibility

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 색상 대비 AA | 일반 텍스트 4.5:1, 대형 텍스트 3:1 | WCAG 2.1 SC 1.4.3 |
| 터치 타겟 | 최소 44×44pt | Apple HIG, WCAG 2.5.8 |
| 포커스 표시 | 인터랙티브 요소에 포커스 인디케이터 존재 | WCAG 2.4.7 |

## Interaction

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 피드백 존재 | 사용자 액션에 시각적 피드백 존재 | NNGroup Feedback |
| 로딩 상태 | 비동기 작업에 로딩 인디케이터 존재 | NNGroup Response Times |
| 에러 표시 | 에러 상태가 명확히 표시됨 | NNGroup Error Messages |

## Motion

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 목적성 | 장식용 애니메이션이 아닌 기능적 목적 존재 | Material Design 3 Motion |
| 듀레이션 | 200~500ms 범위 (너무 빠르거나 느리지 않음) | Apple HIG Motion |
| reduced-motion | prefers-reduced-motion 대응 | WCAG 2.3.3 |

## Visual Hierarchy

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 크기 위계 | 제목/본문/캡션 간 크기 차이가 명확함 (최소 1.2배 이상 비율) | Material Design 3 Typography |
| 대비 강조 | 핵심 콘텐츠가 주변보다 높은 대비를 가짐 | NNGroup Visual Hierarchy |
| 여백 분리 | 그룹 간 여백이 그룹 내 여백보다 넓음 (Gestalt 근접성) | Gestalt 근접성 원칙 |

## Layout & Grid

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 그리드 일관성 | 정의된 그리드 시스템 내에서 요소가 정렬됨 | Material Design 3 Layout |
| 거터 규칙성 | 열 간격(gutter)이 일관된 값을 사용함 | EightShapes Grid |
| 반응형 전략 | 주요 breakpoint에서 레이아웃이 적절히 변환됨 | Apple HIG Layout |

## Ethical Design

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 다크 패턴 부재 | Confirmshaming, Roach Motel, Trick Questions 등 12가지 다크 패턴 미사용 | darkpatterns.org 분류 |
| 동의 명시성 | 체크박스 기본 해제, 이중 부정 문구 미사용 | GDPR, 한국 전자상거래법 |
| 탈퇴 대칭성 | 가입/구독 경로와 해지/탈퇴 경로의 단계 수가 동등함 | EU DSA |

## Authenticity

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 레이아웃 변주 | 연속 섹션이 동일 구조(예: 3열 카드)로 3회 이상 반복하지 않음 | NNGroup State of UX 2026 |
| 컬러 맥락 | 컬러 팔레트가 브랜드/프로젝트에서 도출됨 (제네릭 보라-파랑 기본값 아님) | 925 Studios AI Slop Guide |
| 장식 목적성 | blur, gradient, shadow 등 장식 효과에 기능적 목적 존재 | BSWEN AI UI Anti-Patterns |
| 카피 구체성 | 헤드라인/CTA가 이 제품에만 해당하는 구체적 내용 (범용 문구 아님) | Crea8ive Solution Anti-AI Trends 2026 |
| 이미지 고유성 | 이미지/일러스트가 프로젝트 고유 스타일임 (제네릭 스톡 느낌 아님) | authentic-design.md |
