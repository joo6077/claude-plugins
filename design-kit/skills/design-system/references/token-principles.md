# 토큰 설계 원칙

## 1. 3계층 토큰 구조

> **출처:** [Material Design 3 — Design Tokens](https://m3.material.io/foundations/design-tokens)

| 계층 | 역할 | 예시 |
|------|------|------|
| Reference (원시) | 값 자체 | `blue-500: #2196F3` |
| System (시맨틱) | 역할 기반 매핑 | `primary: ref.blue-500` |
| Component | 컴포넌트별 오버라이드 | `button-bg: sys.primary` |

스킬이 출력하는 토큰 명세는 **System 계층**이다. Reference는 구현 레벨에서 정의하고, Component는 필요 시 toolkit이 생성한다.

## 2. 네이밍 규칙

- semantic 이름만 사용: `primary`, `surface`, `on-primary` ✓
- 값 기반 이름 금지: `blue-500`, `gray-100` ✗
- 크기 스케일은 t-shirt 사이징 또는 숫자 스케일: `sm/md/lg` 또는 `100/200/300`

## 3. 스페이싱 스케일

> **출처:** [Space, Subtraction — Designing Spacing Systems](https://medium.com/eightshapes-llc/space-in-design-systems-188bcbae0d62)

4px 베이스 스케일을 기본으로 한다:
- `xs: 4px`, `sm: 8px`, `md: 16px`, `lg: 24px`, `xl: 32px`, `2xl: 48px`

8px 베이스를 선택할 경우 근거를 명시해야 한다.

## 4. 컬러 시스템

> **출처:** [Apple HIG — Color](https://developer.apple.com/design/human-interface-guidelines/color)

필수 시맨틱 컬러:
- `primary`, `secondary`, `tertiary` — 브랜드/강조
- `surface`, `on-surface` — 배경/텍스트
- `error`, `on-error` — 에러 상태
- `outline`, `outline-variant` — 테두리

다크 모드는 별도 값이 아닌 **동일 토큰의 다크 변형**으로 정의한다.

## 5. 타이포그래피 스케일

> **출처:** [Material Design 3 — Typography](https://m3.material.io/styles/typography)

최소 5단계 스케일:
- `display` — 히어로, 대형 제목
- `heading` — 섹션 제목
- `title` — 카드/리스트 제목
- `body` — 본문
- `label` — 버튼, 캡션

각 단계에 lg/md/sm 서브 사이즈를 둔다.
