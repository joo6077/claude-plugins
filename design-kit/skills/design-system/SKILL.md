---
name: design-system
description: >
  프로젝트에 디자인 토큰 체계(컬러, 타이포, 스페이싱, 라디우스 등)를 세팅한다.
  기존 디자인 시스템이 있으면 리서치 기준과 비교하여 개선점을 제안한다.
  스택 무관 — 원칙만 정의하고, 구체적 코드 생성은 해당 toolkit에 위임한다.
  "디자인 시스템 세팅", "디자인 토큰", "컬러 팔레트 만들어줘",
  "design system init", "토큰 체계" 같은 요청 시 트리거.
  단순 색상 변경, 기존 토큰 값 수정에는 트리거하지 않는다.
argument-hint: "[project-path]"
user-invocable: true
---

# Gotchas

1. **토큰 네이밍에 구체적 값 금지** — `blue-500`, `primary-blue` ✗ → `color.text.primary`, `color.background.brand` ✓. 값이 바뀌면 이름과 괴리가 생기고, 리브랜딩/다크모드 전환 때 즉시 무너진다.
2. **semantic 없이 primitive만 쓰면 안 됨** — `color.green.500`을 컴포넌트에 직접 연결하면 테마 교체가 불가능해진다. 반드시 `primitive → semantic(alias) → component` 3계층을 거쳐야 한다.
3. **다크모드를 토큰 이름에 박지 마라** — `color-dark-text-primary`, `color-light-surface` ✗. 이러면 소비자가 theme-conditional이 된다. semantic 토큰 하나에 mode별 값을 매핑하는 것이 정석이다.
4. **스케일 없이 임의 수치 추가 금지** — `10px, 14px, 18px, 22px`처럼 임의 spacing/radius가 쌓이면 시스템이 무너진다. `2/4/8/12/16/24/32`처럼 유한한 scale을 먼저 확정하고 그 밖은 거부하라.
5. **컴포넌트 토큰을 글로벌처럼 재사용하지 마라** — `button.primary.background`를 다른 컴포넌트에서 끌어 쓰면 결합도가 올라간다. 여러 컴포넌트에 공통으로 필요할 때만 semantic global로 승격하라.
6. **typography는 개별 수치보다 묶음 토큰** — `font-size-14`, `line-height-20`을 각각 쓰면 조합 오류가 생긴다. `font.body.medium`처럼 size/weight/line-height를 묶은 semantic style token을 우선 제공하라.
7. **스페이싱 base 근거 명시 필수** — 4px base가 아니면 반드시 근거를 문서화하라. base 숫자보다 "허용 scale만 사용하는 일관성"이 더 중요하다.
8. **DTCG 금지 문자 사용 주의** — 토큰 이름에 `.` `{` `}` `$` 같은 DTCG 예약 문자를 섞으면 파서 오류가 난다. 경로 구분은 `/` 또는 `.`만 사용하고, `$` 접두사는 메타 키(`$value`, `$type`)에만 허용된다.
9. **스택별 코드 생성 금지** — 이 스킬은 원칙과 토큰 명세만 출력한다. Flutter/React/CSS 코드를 직접 생성하지 마라. 해당 toolkit 플러그인에 위임하라.
10. **HTML 예시 `:root` CSS 변수는 design-kit 기존 파일과 정합해야 한다** — Step 4에서 토큰 명세 예시로 HTML 스니펫을 포함할 경우, `:root { --color-*: ...; }` 값이 `design-kit/docs/` 또는 `design-kit/templates/` 내 기존 HTML 파일의 CSS 변수 값과 일치해야 한다. 값 불일치는 시스템 분열의 시작이며 실제 REJECT 사유였다 (AR-06). 새 변수를 추가할 때는 기존 파일에도 동시에 반영하거나 불일치 이유를 명시하라.

# Process

## Step 1: 프로젝트 디자인 시스템 감지

프로젝트 루트에서 디자인 토큰/테마 파일을 탐색한다:

```text
# 탐색 패턴 (스택 무관)
**/theme/**
**/tokens/**
**/design/**
**/styles/**
**/colors.*
**/typography.*
```

- 발견되면: HAS_DS=true, 기존 토큰 구조를 분석
- 미발견: HAS_DS=false, 신규 토큰 체계 제안 모드

## Step 2: 3계층 토큰 아키텍처 설계

모든 토큰은 아래 3계층으로 분리한다. 계층을 건너뛰어 연결하지 않는다.

```text
Tier 1 — Primitive (값 저장소)
  예: color.palette.green.500 = #22c55e
      space.scale.4 = 4px

Tier 2 — Semantic (역할/의도 alias)
  예: color.text.success → {color.palette.green.500}
      color.background.surface → {color.palette.neutral.50}  (light mode)
      color.background.surface → {color.palette.neutral.900} (dark mode)

Tier 3 — Component (컴포넌트 예외 오버라이드)
  예: button.primary.background → {color.background.brand}
      card.border.radius → {radius.md}
  ※ 여러 컴포넌트에 공통으로 필요해질 때만 Tier 2로 승격
```

카테고리별 필수/선택 및 semantic 네이밍 기준:

| 카테고리 | 필수 여부 | Semantic 예시 | Scale 기준 |
|----------|-----------|---------------|------------|
| Color | 필수 | text.primary, text.secondary, text.disabled, background.surface, background.brand, border.default, border.subtle | — |
| Typography | 필수 | font.display.lg, font.heading.md, font.body.sm, font.label.xs (size+weight+line-height 묶음) | — |
| Spacing | 필수 | space.xs(4), space.sm(8), space.md(16), space.lg(24), space.xl(32), space.2xl(48) | 4px base |
| Radius | 필수 | radius.none(0), radius.sm(4), radius.md(8), radius.lg(16), radius.full(9999) | 유한 scale |
| Elevation | 선택 | elevation.level-0 ~ level-4 (shadow값) | — |
| Motion | 선택 | motion.duration.fast(100ms), motion.duration.normal(200ms), motion.easing.standard | — |

## Step 3: HAS_DS=true → 기존 시스템 분석

기존 토큰을 3계층 아키텍처 기준으로 비교하여 리포트 출력:

- **계층 누락**: primitive를 컴포넌트에 직접 연결한 항목
- **네이밍 위반**: 값이 이름에 포함된 토큰 (`blue-500`, `color-dark-*`)
- **다크모드 미대응**: mode alias가 없는 color semantic 토큰
- **스케일 이탈**: 허용 scale 외 임의 수치 사용
- **컴포넌트 토큰 오남용**: component 토큰을 다른 컴포넌트에서 재사용
- **typography 분리 문제**: size/weight/line-height를 개별 토큰으로만 제공하는 경우

## Step 4: HAS_DS=false → 토큰 명세 생성

templates/design-tokens.md 포맷으로 토큰 명세를 생성한다.
사용자에게 아래 순서로 각 카테고리별 선택지를 제시하고 합의를 받는다:

1. 브랜드 컬러 팔레트 (primitive) 확정
2. semantic color 토큰 — light/dark 양쪽 매핑 포함
3. spacing scale (4px base 기본, 변경 시 근거 명시)
4. typography 스타일 토큰 묶음
5. radius scale
6. elevation/motion (필요 시)

## Step 5: 산출물 확인

- 모든 필수 카테고리가 3계층으로 구분되었는지 확인
- semantic 토큰이 primitive alias로 정의되었는지 확인 (값 직접 기입 ✗)
- light/dark 양쪽 semantic 매핑이 존재하는지 확인
- 허용 scale 외 임의 수치가 없는지 확인
- component 토큰이 있다면 스코프가 해당 컴포넌트로만 제한되었는지 확인
- **:root CSS 변수 정합성 체크** (Gotcha #10) — 산출물에 HTML `:root` 스니펫이 포함된 경우, `design-kit/docs/` 및 `design-kit/templates/` 내 기존 HTML 파일의 CSS 변수 값과 대조하여 불일치 항목이 없는지 확인한다. 불일치 발견 시 기존 파일을 동시에 갱신하거나 이유를 명시한다.

# References

- `references/token-principles.md` — 토큰 설계 원칙 상세
- `templates/design-tokens.md` — 토큰 명세 출력 포맷
