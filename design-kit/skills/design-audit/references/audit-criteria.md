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
