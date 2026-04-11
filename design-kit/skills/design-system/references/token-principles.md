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

## 6. DTCG v1 포맷 (2025-10-28 stable)

> **출처:** [W3C DTCG — Design Tokens Specification Reaches First Stable Version (2025-10-28)](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
> **출처:** [W3C Final Community Group Report — Design Tokens Format Module 2025.10](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/)
> **출처:** [Tokens Studio — Token Format: W3C DTCG vs Legacy](https://docs.tokens.studio/manage-settings/token-format)

Design Tokens Community Group이 2025-10-28에 발표한 **Design Tokens Format Module 2025.10**은 DTCG v1 첫 stable version(Final Community Group Report)이다. W3C Recommendation은 아니지만 Tokens Studio, Style Dictionary, zeroheight 등 주요 툴체인이 이 포맷을 가정한다.

### 핵심 스키마

- **`$value`** — 토큰의 실제 값. 이 키가 있으면 토큰 객체로 인식된다.
- **`$type`** — 토큰 타입(`color`, `dimension`, `fontFamily`, `fontWeight`, `duration`, `cubicBezier`, `shadow`, `gradient`, `typography`, `border`, `transition` 등).
- **`$description`** — 사람이 읽을 설명(선택).
- **`$extensions`** — 툴 벤더 메타데이터 네임스페이스(선택).
- **그룹 객체** — `$value`가 없는 객체는 그룹이며, `$type`을 설정하면 하위 토큰의 기본 타입이 된다.
- **alias** — `{group.token}` dot notation 문자열로 다른 토큰을 참조한다.

### 최소 예시

```json
{
  "$schema": "https://design-tokens.org/schemas/format/2025-10/",
  "color": {
    "$type": "color",
    "brand": {
      "primary": {
        "$value": "oklch(62% 0.18 250)",
        "$description": "브랜드 핵심 CTA 컬러 (OKLCH primitive)"
      }
    },
    "text": {
      "primary": {
        "$value": "{color.brand.primary}",
        "$description": "본문 주요 텍스트 — brand.primary alias"
      }
    }
  },
  "space": {
    "$type": "dimension",
    "md": { "$value": "16px" }
  }
}
```

### 주의 사항

- legacy 포맷의 prefix 없는 `value`/`type` 키는 DTCG v1과 호환되지 않는다.
- 커스텀 `$` prefix 키(`$myMeta` 등)는 피하고 메타데이터는 `$extensions.<vendor>` 아래에 둔다.
- Figma Variables는 OKLCH 미지원이므로, DTCG 토큰에 `oklch()`를 쓰고 Figma 쪽에는 hex 근사치를 병기하는 것이 관행이다.
